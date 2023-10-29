const ipcount = async () => {
    try {
        const response = await fetch('/api/ipcount');
        const data = await response.json();
        const ipCountElement = document.getElementById('ipCount');
        
        if (ipCountElement) {
            ipCountElement.textContent = `Total count of unique visitors: ${data.count}`;
        }
    } catch (e) {
        console.debug('Error while fetching visitor count:\n', e);
    }
}

window.addEventListener("load", ipcount);
