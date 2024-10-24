function initializeTiltEffect() {
    const tiltCards = document.querySelectorAll('.tilt-card');
    const ROTATION_RANGE = 32.5;
    const HALF_ROTATION_RANGE = ROTATION_RANGE / 2;

    tiltCards.forEach(tiltCard => {
        tiltCard.addEventListener('mousemove', (e) => {
            const rect = tiltCard.getBoundingClientRect();
            const width = rect.width;
            const height = rect.height;

            const mouseX = (e.clientX - rect.left) * ROTATION_RANGE;
            const mouseY = (e.clientY - rect.top) * ROTATION_RANGE;

            const rX = (mouseY / height - HALF_ROTATION_RANGE) * -1;
            const rY = mouseX / width - HALF_ROTATION_RANGE;

            tiltCard.style.transform = `rotateX(${rX}deg) rotateY(${rY}deg)`;
        });

        tiltCard.addEventListener('mouseleave', () => {
            tiltCard.style.transform = 'rotateX(0deg) rotateY(0deg)';
        });
    });
}
document.addEventListener("DOMContentLoaded", initializeTiltEffect);