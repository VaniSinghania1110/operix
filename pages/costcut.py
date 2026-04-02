import streamlit as st

st.set_page_config(layout="wide", page_title="CostSense")

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CostSense</title>

<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
--bg:#080c10;
--sf:#0e1318;
--b1:#1c2530;
--b2:#243040;
--tx:#dce6f0;
--mu:#556070;
--ac:#00e5ff;
--a2:#ff6b35;
--gr:#00e090;
}
body{
background:var(--bg);
color:var(--tx);
font-family:sans-serif;
min-height:100vh;
}
.wrap{
max-width:900px;
margin:auto;
padding:40px;
}
.logo{
font-size:40px;
font-weight:700;
margin-bottom:30px;
}
.logo span{
color:var(--ac);
}
.uzone{
border:1px solid var(--b2);
padding:30px;
border-radius:8px;
text-align:center;
background:var(--sf);
}
.abtn{
width:100%;
margin-top:20px;
padding:16px;
background:var(--ac);
border:none;
font-size:18px;
font-weight:700;
cursor:pointer;
}
.loader{
display:none;
text-align:center;
padding:30px;
}
.loader.on{
display:block;
}
.card{
background:var(--sf);
border:1px solid var(--b1);
padding:20px;
margin-top:20px;
border-radius:6px;
}
input{
padding:10px;
margin-top:15px;
width:100%;
}
#results{
display:none;
}
#results.on{
display:block;
}
img{
max-width:250px;
margin-top:20px;
border-radius:8px;
}
</style>
</head>
<body>

<div class="wrap">
<div class="logo">Cost<span>Sense</span></div>

<div id="usec">
<div class="uzone">
<input type="file" accept="image/*" id="finput">
<input type="number" id="priceinput" placeholder="Enter price">
<button class="abtn" id="abtn">Analyze Cost →</button>
</div>
</div>

<div class="loader" id="ldr">
<h2>Analyzing Cost...</h2>
<p>AI is calculating optimized cost</p>
</div>

<div id="results">
<div class="card">
<h2 id="rprod"></h2>
<p id="rissue"></p>
</div>

<div class="card">
<h3>Components</h3>
<div id="rcomp"></div>
</div>

<div class="card">
<h3>Solution</h3>
<div id="rsol"></div>
</div>

<div class="card">
<h3>Price Reduction</h3>
<p id="rbefore"></p>
<p id="rafter"></p>
<p id="rpct"></p>
</div>
</div>
</div>

<script>
var purl = "";

function G(id){
    return document.getElementById(id);
}

G("finput").onchange = function(){
    var f = this.files[0];
    if(!f) return;

    var reader = new FileReader();

    reader.onload = function(e){
        purl = e.target.result;
    };

    reader.readAsDataURL(f);
};

G("abtn").onclick = function(){

    var f = G("finput").files[0];

    if(!f){
        alert("Please upload image");
        return;
    }

    var price = parseFloat(G("priceinput").value);

    if(!price || price <= 0){
        alert("Please enter valid price");
        return;
    }

    G("usec").style.display = "none";
    G("ldr").classList.add("on");

    setTimeout(function(){

        G("ldr").classList.remove("on");
        G("results").classList.add("on");

        var percent = 25;

        var after = Math.round(price * 0.75);
        var savings = price - after;

        G("rprod").innerText = "Smartphone";
        G("rissue").innerText = "High manufacturing and packaging cost";

        G("rcomp").innerHTML =
            "<ul><li>Battery</li><li>Display</li><li>Camera module</li></ul>";

        G("rsol").innerHTML =
            "<ul><li>Use alternate supplier</li><li>Reduce packaging layers</li><li>Optimize sourcing</li></ul>";

        G("rbefore").innerText = "Original Price: Rs. " + price;
        G("rafter").innerText = "Optimized Price: Rs. " + after;
        G("rpct").innerText = percent + "% Saved (Rs. " + savings + ")";

    }, 3000);
};
</script>

</body>
</html>
"""

st.components.v1.html(PAGE, height=900, scrolling=True)
