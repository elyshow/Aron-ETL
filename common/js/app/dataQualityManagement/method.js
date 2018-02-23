/**
 * Created by Administrator on 2016-08-12.
 */
 
/*第一个选项卡*/
$(function(){
	$("#table1").datagrid({
		onSelect:cheBtn,
        onUnselect:cheBtn,
        onSelectAll:cheBtn,
        onUnselectAll:cheBtn,
		url:urls['getMethodList'],
		toolbar:'#metToolBar',
		method:'post',
        autoRowHeight:true,
		columns:[[
			{field:'checkbox',checkbox:true},
			{field:'Method_name',title:'校验方法',align:'center',width:'25%',},
			{field:'Method_type',title:'方法类型',align:'center',width:'15%',},
			{field: 'Predef_method', title: '预定义方法',align:'center', width: '10%'},
			{field:'Createtime',title:'创建时间',align:'center',width:'20%',},
			{field:'oper',title:'操作',align:'center',width:'30%',formatter:operaMethod},
		]], 
		onLoadSuccess:function(){
             // 图标
            $('.detail').linkbutton({
               iconCls: 'icon-search',
            });
			cheBtn();
		},
	});
	$('#methodType').combobox({
		width:200,
        valueField:'id',    //选项值
        textField:"text",   //文本值
		required:true,
        data:[{
            "id":1,
            "text":"格式校验",
        },{
            "id":2,
            "text":"空值校验"
        },{
            "id":3,
            "text":"长度及范围校验"
        },{
            "id":4,
            "text":"代码校验"
        }],
	}); 
	 $('#metSearchBox').searchbox({
        prompt:'请输入校验方法名称搜索',
        height:24,
        width:200,
        searcher:function(v,n){
           $('#table1').datagrid('load', {condition:v,type:1});
        }
    });
})

function cheBtn(){
    var rows = $('#table1').datagrid('getSelections');
    if(rows.length == 0){
        $('#editMetBtn,#delMetBtn').linkbutton('disable')
    }else if(rows.length == 1){
        $('#editMetBtn,#delMetBtn').linkbutton('enable')
    }else{
        $('#editMetBtn').linkbutton('disable')
        $('#delMetBtn').linkbutton('enable')
    }
}

function operaMethod(value, row, index){
	return  '<a class="detail" onClick="methodDetail('+index+')" data-hover="查看详情" title="查看详情"></a>';
}
//新增方法
function addMethodBtn(){
    initDialog('#metDialog', '#table1', '新增');
    $('#id').val('');
}
//修改方法
function editMethodBtn(i){
    var data = getEditData(i, '#table1');
    if(data == false)
        return
    initDialog('#metDialog', '#table1', '修改', data);
}
//删除方法记录
function delMethodBtn(i){
    var data = getDelIDList(i, '#table1');
    if(data == false)
        return
    $.messager.confirm('提示','是否删除选中记录', function(ok){
        if(ok){
            $.post(urls['method_delete'], {ids:data}, function(msg){
                if(msg.errorCode != '0x0000'){
                    $.messager.alert('错误', msg.errorString, 'error')
                }else{
                    $('#table1').datagrid('reload')
                }
            }, 'json')
        }
    })
}
//增加保存提交方法
function addMet(){
	var id = $('input[name="id"]').val();
    console.log(id);
	$('#metForm').form('submit', {
        url:urls['method_save'],
        onSubmit:function(param){
            return $(this).form('validate');
        },
        success:function(msg){
            msg = $.parseJSON(msg);
            if(msg.errorCode != '0x0000'){
                $.messager.alert('错误', msg.errorString, 'error')
            }else{
                $('#metDialog').dialog('close');
                $('#table1').datagrid('reload');
            }
        }
    })
}



//前台详情方法
function methodDetail(i) {
	var data = getEditData(i, '#table1')
    if(data == false)
        return
    initDialog('#detailDialog', '#table1', '查看详情', data);
}
/*function met() {
	$("#detDialog").dialog('close');
	$("#table1").datagrid('reload');
}
//详情对话框中的列表
$(function() {
	$("#parameters").datagrid({
		url: '/parameters/loadList/',
		autoRowHeight: true,
		columns: [[
			{field: 'id', title: '序号', align: 'center', width: '10%',},
			{field: 'parametername', title: '参数名', align: 'center', width: '15%',},
			{field: 'parameterchinese', title: '参数中文名', align: 'center', width: '15%',},
			{field: 'parametertype', title: '参数类型', align: 'center', width: '15%'},
			{field: 'datatype', title: '数据类型', align: 'center', width: '15%',},
			{field: 'defaultvalue', title: '默认值', align: 'center', width: '10%', },
			{field: 'remark', title: '参数说明', align: 'center', width: '10%', },
			{field: 'nonempty', title: '非空', align: 'center', width: '10%', },
		]],
	})
})
//前台检测方法
function metCheck() {
	var row=$("#table1").datagrid('getSelections');
    linkbutton_click('open_dialog',{dialog:'#cheDialog'});
    $('.methodname').val(row[0].methodname);
	$('.checkfun').val(row[0].checkfun);
	$('.methoddetail').val(row[0].methoddetail);

}
function che() {
	$("#cheDialog").dialog('close');
	$("#table1").datagrid('reload');
}
//检测对话框中的列表
$(function() {
	$("#parameters2").datagrid({
		url: '/parameters/loadList2/',
		autoRowHeight: true,
		columns: [[
			{field: 'parametername', title: '参数名', align: 'center', width: '10%',},
			{field: 'parameterchinese', title: '参数中文名', align: 'center', width: '10%',},
			{field: 'datatype', title: '数据类型', align: 'center', width: '15%',},
			{field: 'defaultvalue', title: '默认值', align: 'center', width: '10%', },
		]],
	})
})
//前台增加方法
function addMet() {
	$("#metForm").form('submit', {
		url: "/table1/addData/",
		onSubmit: function () {
					console.log(12)

			return $(this).form('validate');
		},
		success: function (data) {
			$("#metDialog").dialog('close');
			$("#table1").datagrid('reload');

		}
	});
}
function cancel1() {
	$("#metDialog").dialog('close');
	$("#table1").datagrid('reload');
}
//前台删除方法
function metDel() {
	var data = $("#table1").datagrid('getSelections');
	if(data.length == 0){
		$.messager.alert('警告','请至少选择一条数据','warning');
		// return false;
	}
	else{
	$.messager.confirm('确认删除框','是否确定删除选中记录?',function(ok){
		if(ok){
			var ids = '';
			for (var i in data){
				ids += data[i].id + ',';
			}
			ids = ids.substr(0, ids.length -1);
			$.get('/table1/delData/',{data:ids},function(msg){
				$("#table1").datagrid('reload');
			})
		}
	})
		}
}
//前台修改方法
function changeMet() {
	var row=$("#table1").datagrid('getSelections');
	if(row.length==0||row.length>1) {
		$.messager.confirm('警告', '请选择一条数据', 'warning');
	}
		else{
		linkbutton_click('open_dialog',{dialog:'#changeMet'});
		$('.idchange').val(row[0].id);
		$('.methodnamechange').val(row[0].methodname);
		//console.log(row[0].methodname)
		$('.methodtypechange').val(row[0].methodtype);
		$('.predefinedmethodchange').val(row[0].predefinedmethod);
	}
}
//前台修改方法
function table1Preserved() {
	// console.log(222)
	$('#change_list').form('submit', {
		url: "/table1/changeMet/",
		onSubmit: function () {
			return $(this).form('validate');
		},
		success: function (data) {
			$('#changeMet').dialog('close');
			$('#table1').datagrid('reload');
		}
	});
}
function quexiao() {
	$("#cheDialog").dialog('close');
	$("#table1").datagrid('reload');
}*/