// function setOptions() {
//   var option = document.getElementById("id_file_format_0");
//   if (option.checked) {
//     (document.getElementById("id_file_download_1").disabled = true) ; (document.getElementById("id_file_download_3").disabled = true);
//   } 
// } 

// setOptions();


// document.querySelector("input[name=file_format][value=csv]")

// document.getElementById("id_file_format_0").checked


function setOptionsCsv() {
  if (document.querySelector("input[name=file_format][value=csv]").checked) {
    document.querySelector("input[name=file_download][value=all_divide]").disabled = true;
    document.querySelector("input[name=file_download][value=unique_divide]").disabled = true;
  } 
}

function setOptionsXlsx() {
  if (document.querySelector("input[name=file_format][value=xlsx]").checked) {
    document.querySelector("input[name=file_download][value=all_divide]").disabled = false;
    document.querySelector("input[name=file_download][value=unique_divide]").disabled = false;
  } 
}

var csv = document.getElementById("id_file_format_1")
var xlsx = document.getElementById("id_file_format_0")

csv.addEventListener("change",setOptionsCsv);

xlsx.addEventListener("change",setOptionsXlsx);


