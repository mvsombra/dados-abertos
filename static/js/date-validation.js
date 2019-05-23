var hj = new Date();
var dd = hj.getDate();
var mm = hj.getMonth() + 1; //Correção de contagem
var yyyy = hj.getFullYear();

 if(dd < 10){
        dd = '0' + dd
    } 
    if(mm < 10){
        mm = '0' + mm
    } 

hj = yyyy + '-' + mm + '-' + dd;

document.getElementById("inicio").setAttribute("max", hj);
document.getElementById("fim").setAttribute("max", hj);