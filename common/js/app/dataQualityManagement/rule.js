/**
 * Created by Administrator on 2016-08-12.
 */
/*第2个选项卡*/
$(function(){
	$("#table2").datagrid({
		onSelect:checkBtn,
        onUnselect:checkBtn,
        onSelectAll:checkBtn,
        onUnselectAll:checkBtn,
		url:urls['RulesGetRulesList'],
		toolbar:'#rulToolBar',
		method:'post',
        autoRowHeight:true,
		columns:[[
			{field:'checkbox',checkbox:true},
            {field:'Rule_name',title:'规则名称',width:'20%',align:'center'},
            {field:'Object_words',title:'对象类词',width:'15%',align:'center',
				formatter: function(value,row,index){
						return row.Object_words.cname;
				}
			},
            {field:'Identifier',title:'标识符',width:'10%',align:'center',
				formatter: function(value,row,index){
						return row.Identifier.fname;
				}
			},
            {field:'Chinese_name',title:'中文名称',width:'15%',align:'center'},
            {field:'Data_type',title:'数据类型',width:'10%',align:'center'},
			{field:'oper',title:'查看',align:'center',width:'30%',formatter:func2},
		]],  
		onLoadSuccess:function(){
             // 图标
            $('.detail2').linkbutton({
               iconCls: 'icon-search',
            });
			checkBtn();
		},
	})
	
	//对象类词下拉框获取值   选择   标识符与中文名框  联动
	$('#Object_words').combobox({
		valueField:'Object_words',
		textField:'Object_words',
		url:urls['getObject'],
		onSelect:function(record){
			console.log(record);
			$.post(urls['getFieldTable'], {Object_words : record.Object_words}, function(datas){
				console.log(datas);
				var arr = [];
				for(var i = 0; i < datas.length; i++){
					arr.push({ identifier : datas[i].identifier,cnname : datas[i].cnname });
				}	
				console.log(arr);
				$('#Identifier').combobox('clear');
				$('#Chinese_name').combobox('clear');
				$('#Identifier').combobox('loadData',arr);
					
			},'json');
		}
	});
	
	$('#Identifier').combobox({
		valueField:'identifier',    //选项值
        textField:"identifier",	//文本值
		onSelect:function(record){
			console.log(record);
			$.post(urls['getcnname'], {identifier : record.identifier}, function(datas){
				console.log(datas);
				$('#Chinese_name').combobox('readonly');
				$('#Chinese_name').combobox('clear');
				$('#Chinese_name').combobox('setValue',record.cnname);
				$('#dialogTab').datagrid('loadData',datas);
			});
		}
	})
	
	$('#Chinese_name').combobox({
		valueField:'cnname',    //选项值
        textField:"cnname",	//文本值
	});
	
	 $('#rulSearchBox').searchbox({
        prompt:'请输入规则名称搜索',
        height:24,
        width:200,
        searcher:function(v,n){
           $('#table2').datagrid('load', {condition:v,type:1});
        }
    })
	
	//新增弹出框  table数据加载
	$('#dialogTab').datagrid({
        autoRowHeight:true,
		columns:[[
			{field:'checkbox',checkbox:true},
            {field:'csm',title:'参数名',width:'17%',align:'center'},
            {field:'canshu',title:'参数中文名',width:'20%',align:'center'},
            {field:'daty',title:'数据类型',width:'20%',align:'center'},
            {field:'format',title:'参数类型',width:'17%',align:'center'},
            {field:'rule',title:'参数值',width:'15%',align:'center'},
		]],  
	});
})
function checkBtn(){
    var rows = $('#table2').datagrid('getSelections');
    if(rows.length == 0){
        $('#editRuleBtn,#delRuleBtn').linkbutton('disable')
    }else if(rows.length == 1){
        $('#editRuleBtn,#delRuleBtn').linkbutton('enable')
    }else{
        $('#editRuleBtn').linkbutton('disable');
        $('#delRuleBtn').linkbutton('enable');
    }
}

function func2(v,r,i){
	return  '<a data-hover="查看详情" title="查看详情" class="detail2" href="javascript:rulDetail();" data-option=""></a>'
}


//修改规则
function editRuleBtn(index){
    if(index == undefined){
        var row = $('#table2').datagrid('getSelected');
    }else{
        var row = $('#table2').datagrid('getRows')[index];	
    }

    $('#rulDialog').dialog({
        title:'修改',
        onOpen:function(){
			$('input[name="Rule_name"]').val(row.Rule_name);
			$('#Object_words').combobox('select',row.Object_words.cid);
			$('#Identifier').combobox('select',row.Identifier.fid);
			$('input[name="Chinese_name"]').val(row.Chinese_name);
			$('input[name="Data_type"]').val(row.Data_type);
			$('#Rule_type').combobox('select',row.Rule_type.hid);
			$('#Check_method').combobox('select',row.Check_method.tid);
			$('input[name="id"]').val(row.id);
		},
	}).dialog('open');
	$('#table2').datagrid('loadData', { total: 0, rows: [] });
}

//新增规则
function addRuleBtn(index){
    initDialog('#rulDialog', '#table2', '新增');
	$('input[name="id"]').val('');
}

//删除规则记录
function delRuleBtn(i){
    var data = getDelIDList(i, '#table2')
    if(data == false)
        return
    $.messager.confirm('提示','是否删除选中记录', function(ok){
        if(ok){
            $.post(urls['RulesDelete'], {ids:data}, function(msg){
                if(msg.errorCode != '0x0000'){
                    $.messager.alert('错误', msg.errorString, 'error')
                }else{
                    $('#table2').datagrid('reload')
                }
            }, 'json')
        }
    })
}
//提交规则
function addRul(){
	$('#rulForm').form('submit', {
        url:urls['RulesSave'],
        onSubmit:function(index){
          return $(this).form('validate'); 
        },
        success:function(msg){
            msg = $.parseJSON(msg);
            if(msg.errorCode != '0x0000'){
                $.messager.alert('错误', msg.errorString, 'error')
            }else{
				resetContent();
                $('#rulDialog').dialog('close');
				$('#table2').datagrid('reload');
				$('#table2').datagrid('loadData', { total: 0, rows: [] });
            }
        },
    })
}

//表单提交成功后重置表单
function resetContent() {
    var clearForm = document.getElementById('rulForm');
    if (null != clearForm && typeof(clearForm) != "undefined") {
        clearForm.reset();
    }
}

//前台详情方法
function rulDetail(i) {
	$('#detDialog2').dialog({
        onOpen:function(){
			initDialog('#detDialog2', '#table2', '查看详情', data);
            var data = getEditData(i, '#table2');
			console.log(data);
			$('#IdentifierList').combobox('setValues',data.Identifier.fname);
			$('#ruleName').textbox('setText',data.Rule_name);
			$('#chineseName').textbox('setText',data.Chinese_name);
			$('#dataType').textbox('setText',data.Data_type);
			$('#CheckMethodList').combobox('setValues',data.Check_method.tname);
        },
    }).dialog('open')
}
/*function rul() {
	$("#detDialog2").dialog('close');
	$("#table2").datagrid('reload');
}
//前台增加方法
function addRul() {
	$("#rulForm").form('submit', {
		url: "/table2/addData2/",
		onSubmit: function () {
			return $(this).form('validate');
		},
		success: function (data) {
			$("#rulDialog").dialog('close');
			$("#table2").datagrid('reload');

		}
	});
}
//前台删除方法
function rulDel() {
	var data = $("#table2").datagrid('getSelections');
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
			$.get('/table2/delData2/',{data:ids},function(msg){
				$("#table2").datagrid('reload');
			})
		}
	})
		}
}
//前台修改方法
function changeRul() {
	var row=$("#table2").datagrid('getSelections');
	if(row.length==0||row.length>1) {
		$.messager.confirm('警告', '请选择一条数据', 'warning');
	}
		else{
		linkbutton_click('open_dialog',{dialog:'#changeRul'});
		$('.rulenamechange').val(row[0].rulename);
		$('.objectchange').val(row[0].object);
		$('.identifierchange').val(row[0].identifier);
        $('.chinesenamechange').val(row[0].chinesename);
        $('.datatypechange').val(row[0].datatype);
		$('.idchange').val(row[0].id);
		$('.ruletypechange').val(row[0].ruletype);
		$('.methodnamechange').val(row[0].methodname);
	}
}

function table2preserved() {
	$('#change_list2').form('submit', {
		url: "/table2/changeRul/",
		onSubmit: function () {
			return $(this).form('validate');
		},
		success: function (data) {
			$('#changeRul').dialog('close');
			$('#table2').datagrid('reload');
		}
	});
}
//新增对话框中的列表
$(function() {
	$("#parameters21").datagrid({
		url: '/parameters/loadList21/',
		autoRowHeight: true,
		columns: [[
			{field: 'parametername', title: '参数名', align: 'center', width: '10%',},
			{field: 'parameterchinese', title: '参数中文名', align: 'center', width: '10%',},
			{field: 'parametertype', title: '参数类型', align: 'center', width: '15%'},
			{field: 'datatype', title: '数据类型', align: 'center', width: '15%',},
			{field: 'defaultvalue', title: '默认值', align: 'center', width: '10%', },
			{field: 'nonempty', title: '非空', align: 'center', width: '10%', },
		]],
	})
	$("#combobox_type2222").combobox({
        width:130,
        valueField:'id',
        textField:"text",
        data:[{
            "id":  "全部",
            "text": "全部"
        }, {
            "id": "人",
            "text": "人"
        }, {
            "id":"其他",
            "text":"其他"
        }
        ],
    })
$("#combobox_type2223").combobox({
        width:130,
        valueField:'id',
        textField:"text",
        data:[{
            "id": "全部",
            "text": "全部"
        }, {
            "id":"GMSFHM",
            "text":"GMSFHM"
        },{
            "id":"其他",
            "text":"其他"
        }
        ],
    })

$("#combobox_type2224").combobox({
        width:130,
        valueField:'id',
        textField:"text",
        data:[{
            "id": 1,
            "text": "全部"
        }, {
            "id":"长度校验",
            "text":"长度校验"
        },{
            "id":"其他",
            "text":"其他"
        }
        ],
    })

$("#combobox_type2225").combobox({
        width:130,
        valueField:'id',
        textField:"text",
        data:[{
            "id": "全部",
            "text": "全部"
        }, {
            "id":"身份证规范性",
            "text":"身份证规范性"
        },{
            "id":"其他",
            "text":"其他"
        }
        ],
    })
})*/

