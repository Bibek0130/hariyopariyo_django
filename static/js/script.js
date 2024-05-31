// let searchForm = document.querySelector('.search-form');

// document.querySelector('#search-btn').onclick = () =>{
// 	searchForm.classList.toggle('active');
// 	signInForm.classList.remove('active');
// 	shoppingCart.classList.remove('active');
// 	navbar.classList.remove('active');
// }

// let shoppingCart = document.querySelector('.shopping-cart');

// document.querySelector('#cart-btn').onclick = () =>{
// 	shoppingCart.classList.toggle('active');
// 	signInForm.classList.remove('active');
// 	searchForm.classList.remove('active');
// 	navbar.classList.remove('active');
// // }

// let signInForm = document.querySelector('.sign-in-form');

// document.querySelector('#login-btn').onclick = () =>{
// 	signInForm.classList.toggle('active');
// 	shoppingCart.classList.remove('active');
// 	searchForm.classList.remove('active');
// 	navbar.classList.remove('active');
// }

// let navbar = document.querySelector('.navbar');

// document.querySelector('#menu-btn').onclick = () =>{
// 	navbar.classList.toggle('active');
// 	signInForm.classList.remove('active');
// 	shoppingCart.classList.remove('active');
// 	searchForm.classList.remove('active');
// }

// window.onscroll = () =>{
// 	signInForm.classList.remove('active');
// 	shoppingCart.classList.remove('active');
// 	searchForm.classList.remove('active');
// 	navbar.classList.remove('active');
// }

// let slidePosition = 0;
// const slides = document.getElementsByClassName('carousel_item');
// const totalSlides = slides.length;

// // document.getElementById('carousel_button--next').addEventListener("click",function(){moveToNextSlide();});

// // document.getElementById('carousel_button--prev').addEventListener("click",function(){moveToPrevSlide();});

// function updateSlidePosition(){
// 	for(let slide of slides){
// 		slide.classList.remove('carousel_item--visible');
// 		slide.classList.add('carousel_item--hidden');
// 	}
// 	slides[slidePosition].classList.add('carousel_item--visible');
// }

// function moveToNextSlide(){
// 	if(slidePosition === totalSlides-1){
// 		slidePosition = 0;
// 	}else{
// 		slidePosition++;
// 	}
// 	updateSlidePosition();

// }
// function moveToPrevSlide(){
	
// 	if(slidePosition === 0){
// 		slidePosition = totalSlides - 1;
// 	}else{
// 		slidePosition--;
// 	}
// 	updateSlidePosition();
// }

// var swiper = new Swiper(".product-slider", {
//     loop:true,
//     spaceBetween: 20,
//     autoplay: {
//         delay: 7500,
//         disableOnInteraction: false,
//     },
//     centeredSlides: true,
//     breakpoints: {
//       0: {
//         slidesPerView: 1,
//       },
//       768: {
//         slidesPerView: 2,
//       },
//       1020: {
//         slidesPerView: 3,
//       },
//     },
// });

// var swiper = new Swiper(".recipes-slider", {
//     loop:true,
//     spaceBetween: 20,
//     autoplay: {
//         delay: 7500,
//         disableOnInteraction: false,
//     },
//     centeredSlides: true,
//     breakpoints: {
//       0: {
//         slidesPerView: 1,
//       },
//       768: {
//         slidesPerView: 2,
//       },
//       1020: {
//         slidesPerView: 3,
//       },
//     },
// });

// for add to cart functionnality
var updateBtns = document.getElementsByClassName('update-cart')

for(i = 0; i<updateBtns.length; i++){
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action 
		console.log('productId:', productId, 'action', action)
		

		//to ensure if the user is guest user or not
		console.log('USER:', user)
		if(user == 'AnonymousUser'){
			console.log("Not logged in")
		}else{
			updateUserOrder(productId, action)
		}

	})
}

function updateUserOrder(productId, action){
	console.log('user is authenticated , sending data...')

	var url= '/update_item/'

	fetch(url, {
		method: 'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken': csrftoken,
		},
		body:JSON.stringify({'productId':productId, 'action':action})
	})

	.then((response) => {
		return response.json();
	})

	.then((data) => {
		console.log('Data:',data)
		location.reload
	})
}