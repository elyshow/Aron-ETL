window.setInterval(function(){
	var today=new Date();
	var y=today.getFullYear();
	var M=today.getMonth()+1;
	var d=today.getDate();
	var w=today.getDay();
	var h=today.getHours();
	var m=today.getMinutes();
	var s=today.getSeconds();
	if(h < 10){
		h = '0' + h;
	}
	if(m < 10){
		m = '0' + m;
	}
	if(s < 10){
		s = '0' + s;
	}
	
	switch(w){
		case 0:
			if($('.datime').length==1){
				$('.datime')[0].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期日");
			}else{
				$('.datime')[0].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期日");
				$('.datime')[1].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期日");
				$('.datime')[2].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期日");
				$('.datime')[3].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期日");
			}
		break;
		case 1:
			if($('.datime').length==1){
				$('.datime')[0].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期一");
			}else{
				$('.datime')[0].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期一");
				$('.datime')[1].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期一");
				$('.datime')[2].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期一");
				$('.datime')[3].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期一");
			}
		break;
		case 2:
			if($('.datime').length==1){
				$('.datime')[0].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期二");
			}else{
				$('.datime')[0].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期二");
				$('.datime')[1].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期二");
				$('.datime')[2].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期二");
				$('.datime')[3].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期二");
			}
		break;
		case 3:
			if($('.datime').length==1){
				$('.datime')[0].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期三");
			}else{
				$('.datime')[0].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期三");
				$('.datime')[1].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期三");
				$('.datime')[2].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期三");
				$('.datime')[3].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期三");
			}
		break;
		case 4:
			if($('.datime').length==1){
				$('.datime')[0].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期四");
			}else{
				$('.datime')[0].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期四");
				$('.datime')[1].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期四");
				$('.datime')[2].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期四");
				$('.datime')[3].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期四");
			}
		break;
		case 5:
			if($('.datime').length==1){
				$('.datime')[0].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期五");
			}else{
				$('.datime')[0].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期五");
				$('.datime')[1].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期五");
				$('.datime')[2].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期五");
				$('.datime')[3].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期五");
			}
		break;
		case 6:
			if($('.datime').length==1){
				$('.datime')[0].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期六");
			}else{
				$('.datime')[0].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期六");
				$('.datime')[1].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期六");
				$('.datime')[2].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期六");
				$('.datime')[3].innerHTML = (y+"年"+M+"月"+d+"日"+" "+'&nbsp;'+h+":"+m+":"+s+" "+'&nbsp;'+"星期六");
			}
		break;
	}
},1000);


/*$(function(){
	var TbRow = $('.changeColorRow')[0];
	if (TbRow != null){
		for (var i=0;i<TbRow.rows.length ;i++ ){
			if (TbRow.rows[i].rowIndex%2==1){
				TbRow.rows[i].style.backgroundColor="#fff";
			}else{
				TbRow.rows[i].style.backgroundColor="#F1F1F1";
			}
		}
	}
});*/

	