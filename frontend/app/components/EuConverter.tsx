'use client'
import { useCallback, useState } from "react";
import { EnergyUnits, conversion_factors_from_eV, conversion_factors_to_eV } from "../lib/utils/euConverter";

interface EnergyUnitsArrayProps {
    units: EnergyUnits[];
}

export default function EuConverter({ units }: EnergyUnitsArrayProps) {
    const [activeUnit, setActiveUnit] = useState('');
    const [conversionResults, setConversionResults] = useState<Record<string, string>>({});
    const [debounceTimer, setDebounceTimer] = useState<NodeJS.Timeout | null>(null);

    const handleInputChange = useCallback((value: string, activeUnit: EnergyUnits) => {
        if (debounceTimer) {
            clearTimeout(debounceTimer);
        }

        if (!value.trim()) {
            setConversionResults({});
            return;
        }

        const normalizedInput = value.replace(',', '.');
        const realInput = parseFloat(normalizedInput);

        let immediateResults: Record<string, string> = {};
        if (!isNaN(realInput)) {
            immediateResults[activeUnit] = value;
        }
        setConversionResults(immediateResults);

        const newTimer = setTimeout(() => {
            let results: Record<string, string> = { ...immediateResults };

            if (isNaN(realInput)) {
                setConversionResults({});
                return;
            }

            setActiveUnit(activeUnit);

            let sourceConversionFactor = conversion_factors_to_eV[activeUnit];
            if (typeof (sourceConversionFactor) === 'function') {
                sourceConversionFactor = sourceConversionFactor(realInput);
            }
            const valueInEV = sourceConversionFactor * realInput;

            units.forEach((unit) => {
                if (unit !== activeUnit) {
                    let targetConversionFactor = conversion_factors_from_eV[unit];
                    if (typeof (targetConversionFactor) === 'function') {
                        targetConversionFactor = targetConversionFactor(valueInEV);
                    }
                    const finalValue = targetConversionFactor * valueInEV;
                    results[unit] = finalValue.toFixed(10);
                }
            });
            setConversionResults(results);
        }, 300);

        setDebounceTimer(newTimer);
    }, [debounceTimer]);



    const handleInputFocus = (e: React.FocusEvent<HTMLInputElement>, unit: EnergyUnits) => {
        e.target.select()
        setActiveUnit(unit)
    }

    return (
        <section className="w-full h-screen flex flex-col items-center p-5">
            {units.map((unit, index) => (
                <div
                    key={index}
                    className={`p-2 m-2 border rounded-lg shadow flex justify-between items-center ${activeUnit === unit ? 'active' : 'inactive'}`}
                    style={{
                        opacity: activeUnit && activeUnit !== unit ? 0.5 : 1,
                    }}
                >
                    <span className="mr-2">{unit}:</span>
                    <input
                        type="text"
                        className="border p-1 rounded text-black"
                        value={conversionResults[unit] || ''}
                        onChange={(e) => handleInputChange(e.target.value, unit)}
                        onFocus={(e) => handleInputFocus(e, unit)}
                        placeholder={`Enter value in ${unit}`}
                    />
                </div>
            ))}
        </section>
    );
};
