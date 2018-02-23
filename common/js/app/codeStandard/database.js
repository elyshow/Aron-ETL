/**
 * Created by 雷力 on 2016/8/12.
 */

$(function() {
    $("#database_list").datagrid({
        url: '/standardIndex/databaseIndex/getList/',
        columns: [[
            {field: 'checkbox', checkbox: true},
            {field: 'name', title: '数据库名称', width: '50%',},
            {field: 'type', title: '数据库类型', width: '48%',},
        ]]
    })
    
    $('#database_Search').searchbox({
        prompt:'请输入数据库类型搜索',
        height:24,
        width:200,
        searcher:function(v){
           $('#database_list').datagrid('load', {condition:v})
        }
    })
    
})

function database_save(){
    $("#database_form").form('submit',{
        url:'/standardIndex/databaseIndex/saveList/',
        onSubmit:function () {
			console.log($(this).form('validate'));
            return $(this).form('validate');
        },

        success:function (data) {
            $("#database_dialog").dialog('close');
            $("#database_list").datagrid('reload');
        }
    })
}

function database_change() {
    var row=$("#database_list").datagrid('getSelections');
	if(row.length==0||row.length>1) {
		$.messager.confirm('警告', '请选择一条数据', 'warning');
	}
		else{
		linkbutton_click('open_dialog',{dialog:'#database_changedialog'});
		$('#id').val(row[0].id);
		$('.name').val(row[0].name).validatebox('validate');
		$('.type').val(row[0].type).validatebox('validate');
	}
    
}

function preserve_change() {
    $('#database_changeform').form('submit', {
		url:'/standardIndex/databaseIndex/savechangeList/',
		onSubmit: function () {
			console.log($(this).form('validate'));
			return $(this).form('validate');
		},
		success: function (data) {
			$('#database_changedialog').dialog('close');
			$('#database_list').datagrid('reload');
		}
	});
}

function database_del() {
    var data = $("#database_list").datagrid('getSelections');
	if(data.length == 0){
		$.messager.alert('警告','请至少选择一条数据','warning');
	}
	else{
	$.messager.confirm('确认删除框','是否确定删除选中记录?',function(ok){
		if(ok){
			var ids = '';
			for (var i in data){
				ids += data[i].id + ',';
			}
			ids = ids.substr(0, ids.length -1);
			$.post( '/standardIndex/databaseIndex/delDbList/',{data:ids},function(msg){
				$("#database_list").datagrid('reload');
			})
		}
	})
		}
}