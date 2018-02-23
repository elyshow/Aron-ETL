/**
 * Created by Administrator on 2016-08-12.
 */
/*第五个选项卡*/
$(function(){
	$("#table5").datagrid({
		onSelect:stateButton,
        onUnselect:stateButton,
        onSelectAll:stateButton,
        onUnselectAll:stateButton,
		url:urls['getDataTaskMagList'],
		toolbar:'#taskToolBar',
		method:'post',
        autoRowHeight:true,
		columns:[[
			{field:'checkbox',checkbox:true},
			{field:'SchemeName',title:'方案名称',width:'15%',align:'center'},
            {field:'CheckField',title:'校验字段',width:'15%',align:'center'},
            {field:'MethodName',title:'校验方法',width:'15%',align:'center'},
            {field:'SchedulingPlan',title:'调度时间',width:'15%',align:'center'},
            {field:'flag',title:'当前状态',width:'15%',align:'center', formatter: function(value,row,index){
				if (value==0){
					return '未激活';
				}
				if (value==10){
					return '激活';
				}
				if(value==11){
					return '激活/正在执行'
				}
			}},
			{field:'oper',title:'操作',align:'center',width:'25%',formatter:stateFunc},
		]], 
		onLoadSuccess:function(){
             // 图标
           $('.stateStop').linkbutton({
					iconCls: 'icon-no',
				});
				$('.stateStart').linkbutton({
					iconCls: 'icon-ok'
				});
				$('.runNow').linkbutton({
					iconCls: 'icon-tip'
				});
				stateButton();
		},
	})
});






function stateFunc(v,r,i){
	str = ''
	console.log(r);
	// if(r.flag == '0' && r.scheme_type != '1' ){
    if(r.flag == '10'  ){
		str = '<a data-hover="未激活" title="未激活" class="stateStop" href="javascript:;" onclick="stateStop(\''+r.id+'\')" data-options=" " style="margin:8px 5px;"></a>'+
		    '<a data-hover="激活" title="激活" class="stateStart" href="javascript:;" data-options="disabled:true" style="margin:8px 5px;"></a>'+
			'<a data-hover="立即执行" title="立即执行" class="runNow" href="javascript:;" onclick="runNow(\''+r.id+'\')" data-options="" style="margin:8px 5px;"></a>'
	}else if(r.flag == '0' ){
		str = '<a data-hover="未激活" title="未激活" class="stateStop" href="javascript:;" data-options="disabled:true" style="margin:8px 5px;"></a>'+
		    '<a data-hover="激活" title="激活" class="stateStart" href="javascript:;" onclick="stateStart(\''+r.id+'\')" data-options="" style="margin:8px 5px;"></a>'+
			'<a data-hover="立即执行" title="立即执行" class="runNow" href="javascript:;" data-options="disabled:true" style="margin:8px 5px;"></a>'
	}else if(r.flag == '11' ) {
        str = '<a data-hover="未激活" title="未激活" class="stateStop" href="javascript:;" onclick="stateStop(\'' + r.id + '\')" style="margin:8px 5px;"></a>' +
            '<a data-hover="激活" title="激活" class="stateStart" href="javascript:;" data-options="disabled:true" data-options="" style="margin:8px 5px;"></a>' +
            '<a data-hover="立即执行" title="立即执行" class="runNow" href="javascript:;" data-options="disabled:true" style="margin:8px 5px;"></a>'
    }
	// }else if(r.flag == '2' ){
	// 	str = '<a class="stateStop" href="javascript:;" onclick="stateStop(\''+r.id+'\')" data-options=" " style="margin:8px 5px;">未激活</a>'+
	// 	    '<a class="stateStart"  href="javascript:;" onclick="stateStart(\''+r.id+'\')" data-options=" " style="margin:8px 5px;">激活</a>'+
	// 		'<a class="runNow" href="javascript:runNow();" onclick="runNow(\''+r.id+'\')" data-options=" " style="margin:8px 5px;">立即执行</a>'
	// }
    return str;
}


function stateButton(){
    var rows = $('#table5').datagrid('getSelections');
    if(rows.length == 0){
        $('#editTaskBtn').linkbutton('disable')
    }else if(rows.length == 1){
        $('#editTaskBtn').linkbutton('enable')
    }else{
        $('#editTaskBtn').linkbutton('disable');
    }
}
$(function(){
     $("#combobox_type51").combobox({
        width:80,
        valueField:'label',
        textField:"text",
        data:[{
            "label": 1,
            "text": "全部"
        }, {
            "label": 2,
            "text": "基础校验方案"
        },{
            "label":3,
            "text":"其他"
        }
        ],
    })
         $("#combobox_type52").combobox({
        width:80,
        valueField:'label',
        textField:"text",
        data:[{
            "label": 1,
            "text": "全部"
        }, {
            "label": 2,
            "text": "激活"
        }, {
            "label":3,
            "text":"其他"
        }
        ],
    })
         $("#combobox_type53").combobox({
        width:80,
        valueField:'label',
        textField:"text",
        data:[{
            "label": 1,
            "text": "全部"
        }, {
            "label": 2,
            "text": "等待执行"
        }, {
            "label":3,
            "text":"其他"
        }
        ],
    })

	 $('#taskSearchBox').searchbox({
        prompt:'请输入搜索',
        height:24,
        width:200,
        searcher:function(v,n){
           $('#table5').datagrid('load', {condition:v,type:1});
        }
    })

})

//未激活
function stateStop(dataid){
	console.log(dataid);
	$.post(urls['taskMagActivation'],{data:(dataid + ' ' + '0')},function(msg){
		$("#table5").datagrid('reload');
	})
}
// 激活
function stateStart(dataid){
	$.post(urls['taskMagActivation'],{data:(dataid + ' ' + '10')},function(msg){
		$("#table5").datagrid('reload');
	})
}
//立即执行
function runNow(dataid){
	$.post(urls['taskMagActivation'],{data:(dataid + ' ' + '11')},function (ret) {
		$('#table5').datagrid('reload');
	})
}



//前台修改方法
function editTaskBtn() {
	var row=$("#table5").datagrid('getSelections');
	if(row.length==0||row.length>1) {
		$.messager.confirm('警告', '请选择一条数据', 'warning');
	}
	else{
		linkbutton_click('open_dialog',{dialog:'#tasDialog'});
		$('#id').val(row[0].id);
		console.log(row[0].id);
	}
}
//前台修改方法
/*function editTaskBtn() {
	console.log(222)
	 $('#tasDialog').dialog({
        title:'修改',
        onOpen:function(){
			$('input[name="id"]').val();
		},
	}).dialog('open');
}*/

//前台提交方法
function addTas() {
	var id = $('input[name="id"]').val();
	console.log(id);
	
	$("#tasForm").form('submit',{
		queryParams:{ids:id},
		url:urls['saveTaskMag'],
		onSubmit: function () {
			return $(this).form('validate');
		},
		success: function (data) {
			$("#tasDialog").dialog('close');
			$("#table5").datagrid('reload');
		}
	});
}

//取消方法
function cancel5() {
	$('#tasDialog').dialog('close');
	$('#table5').datagrid('reload');
}

$(function () {
	$('#combobox_type552').combobox({
		width: 200,
		valueField: 'id',
		textField: "text",
		data: [{
			"id": "0",
			"text": "未激活"
		}, {
			"id": "2",
			"text": "激活"
		}
		],
	})
})
$(function () {
	$('#combobox_type553').combobox({
		width: 200,
		valueField: 'id',
		textField: "text",
		data: [{
			"id": "0",
			"text": "未激活"
		}, {
			"id": "2",
			"text": "激活"
		}
		],
	})
})

$(function () {
	$('#combobox_type555').combobox({
		width: 200,
		valueField: 'id',
		textField: "text",
		data: [{
			"id": "0",
			"text": "未激活"
		}, {
			"id": "2",
			"text": "激活"
		}
		],
	})
})
$(function () {
	$('#combobox_type558').combobox({
		width: 200,
		valueField: 'id',
		textField: "text",
		data: [{
			"id": 1,
			"text": "全部"
		}, {
			"id": 2,
			"text": "card"
		}
		],
	})
})

//前台删除方法
function tasDel() {
	var data = $("#table5").datagrid('getSelections');
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
				$.get('/table5/delData5/',{data:ids},function(msg){
					$("#table5").datagrid('reload');
				})
			}
		})
	}
}

function initComboBox(start, length){
    var list = [];
    for(var i = 0; i < length; i++,start++){
        list[i] = {};
        list[i].value = "'" +start + "'";
        list[i].text = String(start)
    }
    return list;
}

/*$(function(){
	
	$('#tasForm').delegate( 'input[name="timeType"]', 'change',function(){
        if($(this).is(":checked")){
			$('#days').hide();
			$('#intervalDay').hide();
			$('#once_time').hide();
			
			var index = $(this).index()
		}
		
        switch (index){
            case 0:
                $('.month_day,.play_time').show();
                $('.week_day').hide();
                $('#cycle').next().show().end().combobox('enable').combobox('enableValidation');
                $('#once_time').datetimebox('disableValidation').datetimebox('disable').next().hide();
                $('#hours,#minutes').next().show().end().combobox('enable').combobox('enableValidation');
                $('#intervalDay,#days').combobox('disableValidation').combobox('disable').next().hide();
                $('.words').hide();
                if( $('#cycle').combobox('getValue') == 1 ){
                    $('#days').next().show().end().combobox('enable').combobox('enableValidation');
                    $('.words:eq(0)').show();
					$('#days').css('display','none');
                }else if($('#cycle').combobox('getValue') == 2){
                    $('#days').combobox('disableValidation').combobox('disable').next().hide();
                    $('.week_day').show();
                    $('.words:eq(0)').hide();
					$('#days').hide();
                }else if($('#cycle').combobox('getValue') == 3){
                    $('.words:eq(0)').hide();
					$('#days').hide();
                }else if($('#cycle').combobox('getValue') == ''){
					$('#days').css('display','none');
					$('#intervalDay').css('display','none');
					$('#once_time').css('display','none');
					$('.week_day').css('display','none');
				}
                break;
            case 1:
                $('.month_day').show();
                $('#days,#intervalDay,#cycle,#hours,#minutes').combobox('disableValidation').combobox('disable').next().hide();
                $('.words,.play_time,.week_day').hide();
                $('#once_time').next().show().end().datetimebox('enable').datetimebox('enableValidation');
                break;
            case 2:
                $('#cycle,#days,#intervalDay,#hours,#minutes').combobox('disableValidation').combobox('disable');
                $('#once_time').datetimebox('disableValidation').datetimebox('disable').next().hide();
                $('.month_day,.week_day').hide();
                $('.play_time,.words').hide();
                break;
            case 3:
                $('.month_day,.play_time').show();
                $('#intervalDay,#hours,#minutes').next().show().end().combobox('enable').combobox('enableValidation');
                $('#once_time').datetimebox('disableValidation').datetimebox('disable').hide();
                 $('#cycle,#days').combobox('disableValidation').combobox('disable').next().hide();
                $('.words,.week_day').hide();
                $('.words:eq(1)').show();
                break;
        }
    });
});*/

function selectCycle(record){
    $(this).combobox('checkSelect',$(this));
    switch (record.value){
        case 1:
            $('#days').next().show().end().combobox('enable').combobox('enableValidation');
             $('.words:eq(0)').show();
            $('.week_day').hide();
            break;
        case 2:
            $('#days').combobox('disableValidation').combobox('disable').next().hide();
            $('.week_day').show();
            $('.words:eq(0)').hide();
            break;
        case 3:
            $('.week_day').hide();
            $('#days').combobox('disableValidation').combobox('disable').next().hide();
            $('.words:eq(0)').hide()
            break;
    }
}

