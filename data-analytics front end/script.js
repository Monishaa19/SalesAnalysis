document.addEventListener('DOMContentLoaded', () => {
  const items = Array.from(document.querySelectorAll('input[name="slider"]'));
  const cards = Array.from(document.querySelectorAll('.card'));
  const dynamicButton = document.getElementById('dynamic-button');
  let currentIndex = 0;

  const updateSlider = (direction) => {
      // Uncheck the current radio button
      items[currentIndex].checked = false;

      // Calculate the new index based on direction
      if (direction === 'right') {
          currentIndex = (currentIndex + 1) % items.length;
      } else {
          currentIndex = (currentIndex - 1 + items.length) % items.length;
      }

      // Check the new radio button and update the button
      items[currentIndex].checked = true;
      const activeCard = cards[currentIndex];
      const href = activeCard.dataset.href; // Get the href from the card
      const text = activeCard.dataset.text; // Get the button text from the card

      // Update the button's href and text
      dynamicButton.href = href;
      dynamicButton.textContent = text;
  };



  // Add event listeners for navigation
  document.getElementById('right').addEventListener('click', () => updateSlider('right'));
  document.getElementById('left').addEventListener('click', () => updateSlider('left'));

  // Initialize the button with the first card's href and text
const activeCard = cards[currentIndex];
      const href = activeCard.dataset.href; // Get the href from the card
      const text = activeCard.dataset.text; // Get the button text from the card

      // Update the button's href and text
      dynamicButton.href = href;
      dynamicButton.textContent = text;
});
