


Cookies.set("test", "testy")

function processPayment(cart_data){
    console.log(cart_data)
    console.log(typeof(cart_data))

    //cart_data = document.querySelector('#cart').getAttribute('data-cart')
    //cart_data = JSON.parse(cart_data)
    //console.log(cart_data)
    //console.log(JSON.stringify(cart_data))

    url = '/order/process-order'

    fetch(url, {
        method : 'POST',
        headers : { 'Content-Type' : 'application/json' },
        body : JSON.stringify(cart_data)
    })
    .then(response => {
        if(!response.ok){
            console.log("Response not ok")
        }
        return response.json()
    })
    .then(data =>{
        console.log(data['success'], data['error'])
        if (data['success'] == true){
            console.log("Payment Confirmed")
            
            Cookies.set('paymentComplete', 'true')
            completePayment()
            

            document.querySelector('#process-button').classList.add('hidden')
            document.querySelector('#return-button').classList.remove('hidden')
        }
    })
}

cart_data = document.querySelector('#cart').getAttribute('data-cart')
cart_data = JSON.parse(cart_data)


function calcTotalCost(){
    
    console.log(cart_data)
    totalCost = 0

    Object.values(cart_data).forEach(book => {
        totalCost += (book['price'] * book['quantity'])
    });

    return totalCost
}

totalCost = calcTotalCost()
document.querySelector('#cost-display').textContent = `£${totalCost}`


function completePayment(){
    isComplete = Cookies.get('paymentComplete')

    if (isComplete == 'true'){
        document.querySelector('#process-button').classList.add('hidden')
        document.querySelector('#return-button').classList.remove('hidden')
    
        Cookies.remove('paymentComplete')  // remove cookie
        console.log("running")
    
        // Remove every book from the cart
        url = '/browse-books/remove-all-books-in-cart'
    
        fetch(url, {
            method : "POST",
            headers : {"Content-Type" : "application/json"},
        })
        .then(response => {
            if (!response.ok){
                console.log("Response not ok")
            }
        })
        .then(data => {
            if (data && data['success'] == true){
                console.log(`deleted books in cart`)
            }
        })
        .catch(error => {
            throw new Error(error)
        })
    }
    else{
        Cookies.set('paymentComplete', 'false')
    }
}





