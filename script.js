function updateCriterion(elementId, isValid) {
    const container = document.getElementById(`${elementId}-container`);
    const icon = container.querySelector('.icon');
    
    if (isValid) {
        container.classList.remove('invalid');
        container.classList.add('valid');
        icon.textContent = '✓';
    } else {
        container.classList.remove('valid');
        container.classList.add('invalid');
        icon.textContent = '✗';
    }
}

function updateMeter(strength) {
    const gaugeNeedle = document.getElementById('gauge-needle');
    const strengthText = document.getElementById('strength');
    
    let rotation = '-90deg';
    let color = 'var(--text-muted)';
    let text = 'Awaiting input...';

    switch (strength) {
        case 'Weak':
            rotation = '-60deg';
            color = 'var(--meter-weak)';
            text = 'Weak Password';
            break;
        case 'Moderate':
            rotation = '0deg';
            color = 'var(--meter-moderate)';
            text = 'Moderate Password';
            break;
        case 'Strong':
            rotation = '45deg';
            color = 'var(--meter-strong)';
            text = 'Strong Password';
            break;
        case 'Very Strong':
            rotation = '80deg';
            color = 'var(--meter-strong)';
            text = 'Very Strong Password';
            break;
    }

    if(strength) {
        gaugeNeedle.style.transform = `rotate(${rotation})`;
    } else {
        gaugeNeedle.style.transform = `rotate(-90deg)`;
    }
    strengthText.textContent = text;
    strengthText.style.color = color;
}

function updateSuggestions(password) {
    const suggestionsList = document.getElementById('suggestions-list');
    suggestionsList.innerHTML = '';
    let suggestions = [];

    if (!password) {
        suggestions.push("Start typing to get suggestions...");
    } else {
        if (password.length < 8) {
            suggestions.push("Add more characters. Ensure your password is at least 8 characters long.");
        } else if (password.length < 12) {
            suggestions.push("Aim for 12+ characters for maximum security.");
        }
        if (!/\d/.test(password)) {
            suggestions.push("Include numbers to significantly enhance complexity.");
        }
        if (!/[a-z]/.test(password)) {
            suggestions.push("Add lowercase letters.");
        }
        if (!/[A-Z]/.test(password)) {
            suggestions.push("Include uppercase letters to defend against dictionary attacks.");
        }
        if (!/[^a-zA-Z0-9]/.test(password)) {
            suggestions.push("Add special characters (e.g., !@#$%) to drastically increase crack time.");
        }
        
        if (suggestions.length === 0) {
            suggestions.push("Great job! Your password meets all complexity guidelines.");
        }
    }

    suggestions.forEach(suggestion => {
        let li = document.createElement('li');
        li.textContent = suggestion;
        suggestionsList.appendChild(li);
    });
}

function checkPassword() {
    const password = document.getElementById('password').value;
    
    updateSuggestions(password);

    if (!password) {
        
        updateMeter(null);
        ['length', 'length12', 'numbers', 'lowercase', 'uppercase', 'specialChars'].forEach(id => updateCriterion(id, false));
        document.getElementById('time_to_crack').textContent = '-';
        return;
    }

    
    updateCriterion('length', password.length >= 8);
    updateCriterion('length12', password.length >= 12);
    updateCriterion('numbers', /\d/.test(password));
    updateCriterion('lowercase', /[a-z]/.test(password));
    updateCriterion('uppercase', /[A-Z]/.test(password));
    updateCriterion('specialChars', /[^a-zA-Z0-9]/.test(password));

    
    const data = {
        action: 'evaluate_password',
        password: password
    };

    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        
        if (data.strength) {
            updateMeter(data.strength);
        }
        
        
        const timeToCrack = document.getElementById('time_to_crack');
        if (data.time_to_crack && data.time_to_crack !== 'None') {
            timeToCrack.textContent = data.time_to_crack;
        } else {
            timeToCrack.textContent = '';
        }
    })
    .catch((error) => {
        console.error('Error fetching password evaluation:', error);
    });
}
