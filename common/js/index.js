$(function(){
	$.extend($.fn.validatebox.defaults.rules, {
		// 验证用户名 6-16位 允许字母数字下划线
		username : {
			validator : function(value) { 
				return /^[a-zA-Z][a-zA-Z0-9_]{5,15}$/i.test(value);
			}, 
			message : '用户名不合法（字母开头，允许6-16字节，允许字母数字下划线）' 
		}, 
		// 验证用户姓名 中文或英文
		name : {
			validator : function(value) { 
               return /^[\Α-\￥]+$/i.test(value)|/^\w+[\w\s]+\w+$/i.test(value); 
			}, 
           message : '请输入中文或英文姓名'
		},
		//验证公民18位身份证号码
		idCard : {
			validator : function(value) { 
			   return /^\d{15}(\d{2}[A-Za-z0-9])?$/i.test(value); 
			}, 
			message : '身份证号码格式不正确'
		},
		//验证固定电话或手机号
		phone : {
			validator : function(value){
				return /^(0[0-9]{2,3}\-)?([2-9][0-9]{6,7})+(\-[0-9]{1,4})?$|(^(13[0-9]|15[0|3|6|7|8|9]|18[8|9])\d{8}$)/i.test(value);
			},
			message : '请输入正确的电话号码，如：027-88888888/0728-8888888/15927013197'
		},
		//检查密码和确认密码是否相同
		equals : {    
			validator : function(value,param){    
				return value == $(param[0]).val();    
			},    
			message : '密码匹配错误，请重新输入.'   
		},  
		//匹配肯定包含大写字母和数字组成的8-16位密码
		pwd : {
			validator : function(value){
				return /^(?![a-z0-9]+$)(?![A-Za-z]+$)[A-Za-z0-9]{8,16}$/.test(value);
			},
			message : '请输入包含大写字母与数字组成或大小写字母与数字组成的8-16位密码'
		},
		//匹配只能有汉字和数字的住址（又不全为数字）
		addr : {
			validator : function(value) { 
			   return  /^(?=.*?[\u4E00-\u9FA5])[\d\u4E00-\u9FA5]+/i.test(value); 
			}, 
			message : '请输正确格式的地址' 
		},
		// 验证IP地址
		ips : { 
			validator : function(value) { 
				return /(d+.d+.d+.d+)$/i.test(value); 
			}, 
			message : 'IP地址格式不正确' 
		},
		//电话号码验证
		phones:{
			validator:function(value){
				return /^1[34578]\d{9}$/.test(value);
			},
			message:'电话号码格式不正确'
		},
		//邮箱验证
		email:{
			validator:function(value){
				return /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/.test(value);
			},
			message:'邮箱格式不正确，请输入6~18个字符，包括字母，数字，下划线，以字母开头，字母或数字结尾'
		},
		//微博地址
		urls:{
			validator:function(value){
				return /((http|https|ftp|ftps):\/\/)?([a-zA-Z0-9-]+\.){1,5}(com|cn|net|org|hk|tw)((\/(\w|-)+(\.([a-zA-Z]+))?)+)?(\/)?(\??([\.%:a-zA-Z0-9_-]+=[#\.%:a-zA-Z0-9_-]+(&amp;)?)+)?/.test(value);
			},
			message:'微博地址不正确'
		},
		//所属区域
		area :{
			validator:function(value){
				return /^[A-Za-z0-9]+$ /.test(value);
			},
			message:'只能输入字母，数字，汉字'
		},

	});
	 
});