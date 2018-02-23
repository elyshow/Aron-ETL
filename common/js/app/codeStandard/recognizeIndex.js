$(function(){
	$(".combo_recognize").combobox({
		valueField: 'label',
		textField: 'value',
		data: [{
			label: '1',
			value: '行政'
		},{
			label: '2',
			value: '事业'
		},{
			label: '3',
			value: '政府部门'
		},{
			label:'4',
			value:'军事机构'
		}]

	})
}),
	
	
$(function(){
	$("#recognizeList").datagrid({
		url:'/standardIndex/recognizeIndex/recognInfo/',
		autoRowHeight:true,
		columns:[[
			{field:'checkbox',checkbox:true},
			{field:'name',title:'机构名称',width:'20%',},
			{field:'number',title:'机构编号',width:'20%',},
			{field:'simplename',title:'机构简称',width:'20%',},
			{field:'nature',title:'性质',width:'20%',
			formatter:function (label, row, index) {
				if(label == 1){
					return '行政'
				}else if(label==2){
					return '事业'
				}else if(label==3){
					return '政府部门'
				}else{
					return '军事机构'
				}
			}},
			{field:'oper',title:'操作',width:'18%',formatter:func},
		]],
		onLoadSuccess:function() {
			$('.stateEditor').linkbutton({
				iconCls: 'icon-edit',
			});
		}
	})
	 $('#recSearchBox').searchbox({
        prompt:'请输入机构名称搜索',
        height:24,
        width:200,
        searcher:function(v,n){
           $('#recognizeList').datagrid('load', {condition:v,type:1});
			console.log(v);
			console.log('111');
        }
    })
})

function func(v, r, i) {
	return '<a data-hover="编辑" title="编辑" class="stateEditor" onclick="editRecognData('+ r.id +');"  data-options="" style="margin:8px 5px;"></a>'
}


function editRecognData(id) {
	    $('input[name="save_type"]').val('edit');
        linkbutton_click('open_dialog', {dialog:'#recognizedialog'});
	    $.post('/standardIndex/recognizeIndex/checkData/', {data: id}, function (ret) {
			    $(".combo_recognize").combobox("select", ret[0].recogntype);
				$("#id").val(ret[0].id);
				$("#recognName").val(ret[0].name).validatebox('validate');
				$("#recognNumber").val(ret[0].recognNumber);
				$("#recognSimple").val(ret[0].recognid);
					})
}
//

function recgonAdd() {
	$('input[name="save_type"]').val('add')
	   $('#recognizeForm').form('reset');
	    linkbutton_click('open_dialog' ,{dialog: '#recognizedialog'});
}


function recognizeClose() {
	$('#recognizedialog').dialog('close');
}

function recognSub() {
	
	$('#recognizeForm').form('submit', {
		url: "/standardIndex/recognizeIndex/recognAddData/",
		onSubmit: function () {
			var isValid = $(this).form('validate');
			console.log(isValid);
			return isValid;
		},
		success: function (data) {
			$('#recognizedialog').dialog('close');
			$('#recognizeList').datagrid('reload');
		}
	});
}


function recgonDel() {
    var data = $("#recognizeList").datagrid('getSelections');
	if (data.length == 0) {
		$.messager.alert('警告', '请选择至少一条数据', 'warning');
	}
	else {
		$.messager.confirm('确认删除框', '是否确定删除选中记录?', function (ok) {
			if (ok) {
				var ids = '';
				for (var i in data) {
					ids += data[i].id + ',';
				}
				ids = ids.substr(0, ids.length - 1);
				console.log(ids)
				$.post('/standardIndex/recognizeIndex/recognDel/', {data: ids}, function (msg) {
					$('#recognizeList').datagrid('reload');
				})
			}
		})
	}
}