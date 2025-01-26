const gifContainer = document.getElementById("gifContainer");
const gifImage = gifContainer.querySelector("img");
const containerWidth = 100; // Width of the container (matches CSS)
const speed = 2; // Adjust speed (pixels per frame)

let positionX = 0;
let direction = 1; // 1 for right, -1 for left

function moveGIF() {
    const windowWidth = window.innerWidth;

    // Update position
    positionX += speed * direction;

    // Flip direction if at the edges
    if (positionX + containerWidth >= windowWidth || positionX <= 0) {
        direction *= -1;
        gifImage.style.transform = `scaleX(${direction})`; // Flip the GIF
    }

    // Move the GIF container
    gifContainer.style.left = `${positionX}px`;

    requestAnimationFrame(moveGIF);
}

// Initialize animation
moveGIF();