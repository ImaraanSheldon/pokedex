        // Create fireflies dynamically
        const numFireflies = 15; // Number of fireflies

        for (let i = 0; i < numFireflies; i++) {
            const firefly = document.createElement('div');
            firefly.classList.add('firefly');

            // Randomize animation and positions
            firefly.style.setProperty('--x', Math.random());
            firefly.style.setProperty('--y', Math.random());
            firefly.style.animationDuration = `${Math.random() * 8 + 8}s`;

            document.body.appendChild(firefly);
        }