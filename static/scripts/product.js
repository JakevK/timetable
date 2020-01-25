function product() {
  let xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {updateContent(this.response)};
  xhttp.open("GET", "/prod");
  xhttp.setRequestHeader("Content-type", "application/json; charset=utf-8");
  xhttp.send();
}

function updateContent(response) {
  console.log(response);
}

() => {

}
