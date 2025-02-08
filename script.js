var sections = document.querySelectorAll('div.box');
const sectionNumber = document.getElementById('sectionNumber');
var currentSection = sections.length - 1;
sectionNumber.innerHTML = currentSection + 1;

window.onload = function() {
    if (sections.length > 0) {
        sections[sections.length - 1].scrollIntoView({ behavior: 'auto' });
    }
};

// Search button
const searchInput = document.getElementById('searchInput');
searchInput.addEventListener('input', function() {
    const searchTerm = this.value.toLowerCase();
    sections = document.querySelectorAll('div.box');
    sections.forEach(section => {
        if (section.textContent.toLowerCase().includes(searchTerm)) {
            section.style.display = 'block';
        } else {
            section.style.display = 'none';
        }
    });
    sections = Array.from(sections).filter(box => {
        return window.getComputedStyle(box).display === 'block';
    });
    console.log(sections.length);
    if (sections.length > 0) {
        sections[sections.length - 1].scrollIntoView({ behavior: 'auto' });
        currentSection = sections.length - 1;
        sectionNumber.innerHTML = currentSection + 1;
    }
});

// Copy source code func
const codeBlocks = document.querySelectorAll('code[class^="language-"]');
codeBlocks.forEach(codeBlock => {
    const sourceCodeDiv = document.createElement('div'); 
    sourceCodeDiv.className = 'sourceCodeDiv';
    codeBlock.parentNode.insertBefore(sourceCodeDiv, codeBlock);
    sourceCodeDiv.appendChild(codeBlock);

    const copyButton = document.createElement('span');
    copyButton.className = 'copy-button';
    const icon = document.createElement('i');
    icon.className = 'fas fa-copy';
    copyButton.appendChild(icon);
    sourceCodeDiv.insertBefore(copyButton, sourceCodeDiv.firstChild);
    
    copyButton.addEventListener('click', () => { 
        copyButton.style.color = '#00FFEB';
        setTimeout(() => {
            copyButton.style.color = '';
        }, 200);
        const textToCopy = sourceCodeDiv.textContent; 
        tempTextArea = document.createElement('textarea'); 
        tempTextArea.value = textToCopy; 
        document.body.appendChild(tempTextArea);
        tempTextArea.select(); 
        document.execCommand('copy'); 
        document.body.removeChild(tempTextArea); 
    });
});

// Scroll functions
document.getElementById('scrollTop').addEventListener('click', function() {
    sections[0].scrollIntoView({ behavior: 'auto' });
    currentSection = 0;
    sectionNumber.innerHTML = currentSection + 1;
});

document.getElementById('scrollToBottom').addEventListener('click', function() {
    if (sections.length > 0) {
        sections[sections.length - 1].scrollIntoView({ behavior: 'auto' });
        currentSection = sections.length - 1;
        sectionNumber.innerHTML = currentSection + 1;
    }
});

// Scroll step by step
function scrollToSection(direction) {
    currentSection += direction;
    if (currentSection < 0) {
        currentSection = 0;
    } else if (currentSection >= sections.length) {
        currentSection = sections.length - 1;
    }
    sections[currentSection].scrollIntoView({ behavior: 'smooth' });
    sectionNumber.innerHTML = currentSection + 1;
}

function scrollToCurrentSection() {
    sections[currentSection].scrollIntoView({ behavior: 'smooth' });
}   

// Hide/Show tools
const scrollTop = document.getElementById('scrollTop');
const scrollToBottom = document.getElementById('scrollToBottom');
const scrollStepUp = document.getElementById('scrollStepUp');
const scrollStepDown = document.getElementById('scrollStepDown');

document.addEventListener('mousemove', function(event) {
    const mouseX = event.clientX;
    const windowWidth = window.innerWidth;
    if (windowWidth - mouseX < 40) {
        scrollTop.style.display = 'block';
        scrollToBottom.style.display = 'block';
        scrollStepUp.style.display = 'block';
        scrollStepDown.style.display = 'block';
        sectionNumber.style.display = 'block';
        openSearch.style.display = 'block';
    } else {
        scrollTop.style.display = 'none';
        scrollToBottom.style.display = 'none';
        scrollStepUp.style.display = 'none';
        scrollStepDown.style.display = 'none';
        sectionNumber.style.display = 'none';
        openSearch.style.display = 'none';
    }
});

searchInput.style.display = 'none';
function opensearch() {
    if (searchInput.style.display === 'none') {
        searchInput.style.display = 'block';
    } else {
        searchInput.style.display = 'none';

    }
}