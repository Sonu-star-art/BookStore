


function delete_book(book_id){
    fetch('/update-books/delete-book', {
        method : 'POST',
        headers : { 'Content-Type' : 'application/json' },
        body : JSON.stringify(book_id)
    })
    .then(response=>{
        if (!response.ok){
            console.log('response not ok')
            return
        }
        return response.json()
    })
    .then(data=>{
        if (data['success'] == true){
            window.location.href = "/update-books"  // if book deleted successfully, go back to update books route
        }
    })
    
}

