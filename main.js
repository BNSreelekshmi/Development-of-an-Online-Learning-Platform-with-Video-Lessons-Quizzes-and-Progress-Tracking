document.addEventListener('DOMContentLoaded', function() {

    // ---------- Quiz Submission Alert ----------
    const quizForm = document.querySelector('form');
    if (quizForm) {
        quizForm.addEventListener('submit', function() {
            alert('Your answer has been submitted!');
        });
    }

    // ---------- Highlight Selected Answer ----------
    const radios = document.querySelectorAll('input[type="radio"]');
    radios.forEach(radio => {
        radio.addEventListener('change', function() {
            radios.forEach(r => r.parentElement.style.backgroundColor = '');
            this.parentElement.style.backgroundColor = '#d1e7dd';
        });
    });

    // ---------- Animate Buttons ----------
    const buttons = document.querySelectorAll('button, a.button');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
            this.style.transition = 'transform 0.2s';
        });
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // ---------- Progress Bars ----------
    const bars = document.querySelectorAll('.progress-bar');
    bars.forEach(bar => {
        let value = bar.getAttribute('data-progress');
        setTimeout(() => { bar.style.width = value + '%'; }, 500);
    });
});