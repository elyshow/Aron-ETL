$(function(){
	$('#search').searchbox({
        prompt:'请输入目录或资源名称',
        height:24,
        width:200,
        searcher:function(v,n){
           $('#test').datagrid('load', {condition:v})
        }
    })
})



function chkNumber(eleText) {
 	var value =eleText.value; 
	var len=value.length; 
	for(var i=0;i<len;i++){
         if(value.charAt(i)>"9"||value.charAt(i)<"0") { 
			alert("含有非数字字符");
			eleText.value="";
			eleText.focus(); 
			break; 
         }
    }
} 


function checkGoBtn() {
	var goPage = document.getElementById("goPage");
	var numReg = /^[0-9]+$/g; //纯数字正则表达式

	/*var numRegOk = numReg.test(goPage.val());*/
	if (goPage.value == "" || goPage.value == 0 || goPage == numReg) {
		goPage.value="";
		return false;
	
	}
}