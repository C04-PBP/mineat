function initializeTiltEffect() {
    const tiltCards = document.querySelectorAll('.tilt-card');
    const ROTATION_RANGE = 36;
    const PARALLAX_DEPTH = 10; 

    tiltCards.forEach(tiltCard => {
        const imageContainer = tiltCard.querySelector('.image-container img');

        tiltCard.addEventListener('mousemove', (e) => {
            const rect = tiltCard.getBoundingClientRect();
            const width = rect.width;
            const height = rect.height;

            const mouseX = (e.clientX - rect.left) * ROTATION_RANGE;
            const mouseY = (e.clientY - rect.top) * ROTATION_RANGE;

            const rX = (mouseY / height - ROTATION_RANGE / 2) * -1;
            const rY = mouseX / width - ROTATION_RANGE / 2;

            // Apply rotation to the tilt card
            tiltCard.style.transform = `rotateX(${rX}deg) rotateY(${rY}deg)`;

            // Apply a smaller parallax movement to the image
            const parallaxX = rY / PARALLAX_DEPTH;
            const parallaxY = rX / PARALLAX_DEPTH;
            imageContainer.style.transform = `translateX(${parallaxX}px) translateY(${parallaxY}px)`;
        });

        tiltCard.addEventListener('mouseleave', () => {
            tiltCard.style.transform = 'rotateX(0deg) rotateY(0deg)';
            imageContainer.style.transform = 'translateX(0px) translateY(0px)';
        });
    });
}
document.addEventListener("DOMContentLoaded", initializeTiltEffect);
