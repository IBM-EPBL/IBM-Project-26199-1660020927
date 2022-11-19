function searchbarr() {
    let input = document.getElementById('searchbar').value
    input=input.toLowerCase();
    let x = document.getElementsByClassName('srchbar');
    let y;
    for (i = 0; i < x.length; i++) { 
        if (!x[i].innerHTML.toLowerCase().includes(input)) {
            x[i].style.display="none"; 
        }
        else {
           
            y=x[i].innerHtml+".html"
            window.open("/y");                 
        }
    }
}