// function removeFromCart(productId) {
//     if (confirm("Are you sure you want to remove this item?")) {
//       fetch(`/cart/remove/${productId}/`, {
//         method: "POST",
//         headers: {
//           "X-CSRFToken": "{{ csrf_token }}",
//           "Content-Type": "application/json",
//         },
//         credentials: "same-origin",
//       })
//         .then((response) => response.json())
//         .then((data) => {
//           if (data.success) {
//             // Remove item row with animation
//             const itemRow = document.getElementById(`cart-item-${productId}`);
//             itemRow.style.transition = "all 0.3s";
//             itemRow.style.opacity = "0";

//             setTimeout(() => {
//               itemRow.remove();
//               updateCartSummary(); // This now handles all updates
//             }, 300);
//           }
//         })
//         .catch((error) => console.error("Error:", error));
//     }
//   }

  function updateCartSummary() {
    fetch("/cart/summary/")
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          // Update items count
          document.getElementById("summary-items-count").textContent =
            data.items_count;

          // Update subtotal and total
          document.getElementById("summary-subtotal").textContent =
            data.total_price;
          document.getElementById("summary-total").textContent =
            data.total_price;

          // Update cart counter in navbar
          const cartCount = document.querySelector(".cart-count");
          if (cartCount) {
            cartCount.textContent = `(${data.items_count})`;
          }
        }
      })
      .catch((error) => console.error("Error:", error));
  }

//   function updateQuantity(productId, change) {
//     const quantityElement = document.getElementById(`quantity-${productId}`);
//     let newQuantity = parseInt(quantityElement.textContent) + change;

//     if (!isNaN(newQuantity)) {
//       newQuantity = Math.max(1, newQuantity); // Ensure quantity ≥ 1

//       fetch(`/cart/update/${productId}/`, {
//         method: "POST",
//         headers: {
//           "X-CSRFToken": "{{ csrf_token }}", //document.querySelector("[name=csrfmiddlewaretoken]").value,
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify({
//           quantity: newQuantity,
//         }),
//         credentials: "include",
//       })
//         .then((response) => {
//           if (!response.ok) {
//             if (response.status === 406) {
//               // handle 406 specifically
//               alert("Quantity exceeds available stock!");
//               throw new Error("Quantity exceeds available stock!");
//             } else if (response.status === 400) {
//               alert("Quantity must be at least 1");
//               throw new Error("Quantity must be at least 1");
//             } else {
//               throw new Error("Network response was not ok");
//             }
//           }
//           return response.json();
//         })
//         .then((data) => {
//           if (data.success) {
//             quantityElement.textContent = data.quantity;
//             updateRowTotal(productId, data.quantity);
//             updateCartSummary();
//             toggleMinusButton(productId, data.quantity);
//             toggleplusButton(productId, data.quantity);
//           } else {
//             throw new Error(data.error || "Update failed");
//           }
//         })
//         .catch((error) => {
//           console.error("Error:", error);
//           // alert("Failed to update quantity. Please try again.");
//         });
//     } else {
//       alert("Do not play with code! ;)");
//     }
//   }
  function updateRowTotal(productId, quantity) {
    const itemRow = document.getElementById(`cart-item-${productId}`);
    const price = parseFloat(
      itemRow.querySelector("td:nth-child(2)").textContent.replace("£", "")
    );
    itemRow.querySelector(".item-total").textContent = `£${(
      price * quantity
    ).toFixed(2)}`;
  }

  function toggleMinusButton(productId, quantity) {
    const minusBtn = document
      .getElementById(`cart-item-${productId}`)
      .querySelector(".minus");
    minusBtn.disabled = quantity <= 1;
  }

  function toggleplusButton(productId, quantity) {
    const plusBtn = document
      .getElementById(`cart-item-${productId}`)
      .querySelector(".plus");
    plusBtn.disabled =
      quantity >=
      parseInt(document.querySelector(`#available-${productId}`).textContent);
  }