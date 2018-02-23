$.extend($.fn.validatebox.defaults,{
	delay:50,
});
$.extend($.fn.datagrid.defaults,{
	fit:true,
	pagination:true,
	border:false,
	autoRowHeight:false,
	striped:true,
	rowStyler:function(){
		return 'line-height:25px;'
	},
	onHoverCell:function(index,field, value,type,t){
		var options = $(this).datagrid('getColumnOption',field)
		if(options.showTitle == true){
			t.attr('title', value)
		}
	},
});
$.extend($.fn.datagrid.methods,{
	checkRow:function(jq,condition){
		var data = jq.datagrid('getData').rows;
		var fields = jq.datagrid('getColumnFields');
		if(condition == ''){
			jq.datagrid('loadData', data);
			return;
		}
		for(var i in data){
			var flag = false;
			for(var j = 1; j< fields.length - 1; j++){
				if(data[i][fields[j]].toLowerCase().indexOf(condition.toLowerCase()) != -1 ){
					flag = true;
					break;
				}
			}
			jq.datagrid('hideOrShowRow',{index:i, status: flag});
		}
	},
	hideOrShowRow:function(jq, param){
		var row =jq.prev().find('.datagrid-body tr').eq(param.index);
		if(param.status)
			row.show();
		else
			row.hide();
	},
	getValueByField:function(jq,field){
		var data = jq.datagrid('getData').rows;
		var list = [];
		for(var i in data){
			list.push(data[i][field]);
		}
		return list;
	}
});

$.extend($.fn.textbox.defaults,{
	onFocus:function(value){

	},
	onBlur:function(value){

	}
});


$.extend($.fn.dialog.defaults,{
	closed:true,
	shadow:true,
	modal:true,
})

$.extend($.fn.combobox.defaults,{
	prompt:'请选择...',
	width:input_width,
	height:input_height,
	panelHeight:'auto',
	panelMinHeight:24,
	panelMaxHeight:200,
	editable:true,
	values:[],
	//delay:1000,
	filter:function(value,row){
		var opts = $(this).combobox('options');
		return row[opts.textField].indexOf(value) > -1 ;
	},
	onShowPanel:function(){
		$(this).combobox('reloadData');
	},
	onFocus:function(value){
		$(this).combobox('showPanel');
	},
	onBlur:function(value){

	},
	onHidePanel:function(){
		var t = $(this),
			data = t.combobox('getData'),
			opts = t.combobox('options'),
			values = opts.values,
			value = t.combobox('getText');
		if(values.length != 0)
			values = []
		for(var i = 0 ; i< data.length; i++)
			values.push(data[i][opts.textField])
		if(opts.multiple != true){
			if($.inArray(value,values) == -1 && value != ''){
				$.messager.alert('警告','输入的值不符合要求,请重新输入','warning',function(){
					t.combobox('select','');
				})
			}
		}else{
			var allValue = value.split(',')
			for(var i in allValue)
				if($.inArray(allValue[i],values) == -1 && allValue[i] != ''){
					$.messager.alert('警告','输入的值不符合要求,请重新输入','warning',function(){
						t.combobox('setValues', '').combobox('setText','').combobox('select','');
					})
				}
		}
	},
	onSelect:function(record){
		$(this).combobox('checkSelect');
	},
})

$.extend($.fn.combobox.methods,{
	checkSelect:function(jq){
		if(jq.combobox('getText') === '请选择...' || jq.combobox('getValue') === ''){
			jq.combobox('setText','');
		}
	},
	reloadData:function(jq){
		var opts = jq.combobox('options'),data = opts.data || jq.combobox('getData'),choice = {};
		choice[opts.textField] = '请选择...';
		choice[opts.valueField] = '';

		if(data != undefined && data != null) {
			if (data.length != 0) {
				if (choice[opts.textField] == data[0][opts.textField]) {
					return;
				}
			} else {
				data = [];
			}
		}else{
			data = [];
		}
		data.unshift(choice);
		jq.combobox('loadData',data).combobox('checkSelect');
	},
	reloadValue:function(jq,list){

	}
})

$.extend($.fn.textbox.defaults,{
	width:input_width,
	height:input_height,
})

$.extend($.fn.linkbutton.methods,{
	open_dialog:function(jq,obj){
		$.fn.linkbutton('check_obj',obj)
		$(obj.dialog).dialog('open');
	},
	saveChange:function(jq,obj){
		$.fn.linkbutton('check_obj',obj);
		$(obj.form).form('submit',{
			url:obj.url,
			onSubmit:function(param){
				if(obj.param){
					for(var i in obj.param)
						param[i] = obj.param[i];
				}
				return $(this).form('validate');
			},
			success:function(msg){
				msg = $.parseJSON(msg);
				if(msg.errorCode != '0x0000'){
					$.messager.alert('错误',msg.errorString,'error');
				}else{
					$(obj.dialog).dialog('close')
					$(obj.datagrid).datagrid('reload');
				}
			}
		})
	},
	check_obj:function(jq,obj){
		if(obj == undefined){
			console.error('function add request one param,but nothing given!');
			return false;
		}
	}
})
