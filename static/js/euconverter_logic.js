const unitConversions = {
    Hartrees: 1,
    eV: 0.03674930495120813,       // 1 Hartree = 27.2114 eV
    kJ_per_mol: 0.0003808798033989866, // 1 Hartree = 2625.5 kJ/mol
    kcal_per_mol: 0.0015936010974213599, // 1 Hartree = 627.5095 kcal/mol
    cm_minus1: 0.0000045563352812122295, // 1 Hartree = 219474.63 cm^-1
    nm_minus1: 45.5633528121223 // 1 Hartree = 0.021947463 nm^-1
}

const energyConverter = (value, sourceUnit, targetUnit) => {
    if (!isNaN(value)) {
        return parseValue(
            (value * (unitConversions[sourceUnit] / unitConversions[targetUnit]))
            .toPrecision(10)
        );
    }
    return ""
}

// Pure function to convert input values to floats
const parseValue = (value) => parseFloat(value.replace(',', '.'));

// Higher order function to create input handler
const createInputHandler = (inputFields) => (event) => {
    const inputField = event.target;
    const value = parseValue(inputField.value);
    const sourceUnit = inputField.getAttribute('data-unit');

    inputFields.forEach(targetField => {
        const targetUnit = targetField.getAttribute('data-unit');
        if (targetField !== inputField) {
            targetField.value = energyConverter(value, sourceUnit, targetUnit);
        }
    });
};

const inputFields = document.querySelectorAll('.input-field');
const inputHandler = createInputHandler(inputFields);

inputFields.forEach(inputField => {
    inputField.addEventListener('input', inputHandler);
});
