var updateBtns = document.getElementsByClassName("update-cart");

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener("click", function () {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log("productId:", productId, "Action:", action);
        updateUserOrder(productId, action);
    });
}

function updateUserOrder(productId, action) {
    console.log("User is authenticated, sending data...");

    var url = "/update_item/";

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ productId: productId, action: action }),
    })
        .then((response) => {
            if (response.status === 403) {
                window.location.href = "/login/";
                return;
            }
            return response.json();
        })
        .then((data) => {
            if(data){
                location.reload();
            }
        });
}
