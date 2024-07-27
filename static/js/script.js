
// for add to cart functionnality
// var updateBtns = document.getElementsByClassName('update-cart')

// for(i = 0; i<updateBtns.length; i++){
// 	updateBtns[i].addEventListener('click', function(){
// 		var productId = this.dataset.product
// 		var action = this.dataset.action 
// 		console.log('productId:', productId, 'action', action)
		

// 		//to ensure if the user is guest user or not
// 		console.log('USER:', user)
// 		if(user == 'AnonymousUser'){
// 			addCookieItem(productId, action)
// 		}else{
// 			updateUserOrder(productId, action)
// 		}

// 	})
// }

// function addCookieItem(productID, action){
// 	console.log("Not Logged in ")

// 	if (action == 'add'){
// 		if (cart[productID] == undefined){
// 			cart[productID] = {'quantity': 1};

// 		}else{
// 			cart[productID]['quantity'] += 1;
// 		}
// 	}
// 	if (action == 'remove'){
// 		cart[productID]['quantity'] -= 1;

// 		if (cart[productID]['quantity'] <= 0){
// 			console.log('Remove Item');
// 			delete cart[productID];
// 		}
// 	}
// 	console.log('Cart: ',cart)
// 	document.cookie = 'cart =' + JSON.stringify(cart) + ";domain=;path=/"
// 	location.reload();

// }

// function updateUserOrder(productId, action){
// 	console.log('user is logged in, sending data...')

// 	var url= '/update_item/'

// 	fetch(url, {
// 		method: 'POST',
// 		headers:{
// 			'Content-Type':'application/json',
// 			'X-CSRFToken': csrftoken,
// 		},
// 		body:JSON.stringify({'productId':productId, 'action':action})
// 	})

// 	.then((response) => {
// 		return response.json();
// 	})

// 	.then((data) => {
		
// 		location.reload();
// 	});
// }
document.addEventListener('DOMContentLoaded', function() {
    var updateBtns = document.getElementsByClassName('update-cart');

    for (let i = 0; i < updateBtns.length; i++) {
        updateBtns[i].addEventListener('click', function() {
            var productId = this.dataset.product;
            var action = this.dataset.action;
            console.log('productId:', productId, 'action:', action);

            // To ensure if the user is a guest user or not
            console.log('USER:', user);
            if (user === 'AnonymousUser') {
                addCookieItem(productId, action);
            } else {
                updateUserOrder(productId, action);
            }
        });
    }
});

function addCookieItem(productId, action) {
    console.log("Not Logged in ");

    if (action === 'add') {
        if (cart[productId] === undefined) {
            cart[productId] = {'quantity': 1};
        } else {
            cart[productId]['quantity'] += 1;
        }
    }
    if (action === 'remove') {
        cart[productId]['quantity'] -= 1;

        if (cart[productId]['quantity'] <= 0) {
            console.log('Remove Item');
            delete cart[productId];
        }
    }
    console.log('Cart: ',cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
    location.reload();
}

function updateUserOrder(productId, action) {
    console.log('User is logged in, sending data...');

    var url = '/update_item/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action}),
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        location.reload();
    });
}
