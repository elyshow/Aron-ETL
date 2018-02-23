/**
 * Created by Administrator on 2016-08-12.
 */
/*第3个选项卡*/
$(function(){
	$("#table3").datagrid({
		onSelect:checkBaseBtn,
        onUnselect:checkBaseBtn,
        onSelectAll:checkBaseBtn,
        onUnselectAll:checkBaseBtn,
		url:urls['getBasicTestingList'],
		toolbar:'#basToolBar',
		method:'post',
        autoRowHeight:true,
		columns:[[
			{field:'checkbox',checkbox:true},
         	{field:'schemeName',title:'方案名称', width:'20%',align:'center'},
			{field:'checkObject',title:'校验对象', width:'20%',align:'center'},
			{field:'checkRule',title:'校验方法', width:'20%',align:'center'},
			{field:'executionDate',title:'执行时间', width:'20%',align:'center'},
			{field:'oper',title:'查看',align:'center',width:'20%',formatter:func3},
		]],  
		onLoadSuccess:function(){
             // 图标
            $('.detail3').linkbutton({
               iconCls: 'icon-search',
            });
			checkBaseBtn();
		},
	})

	 $('#basSearchBox').searchbox({
        prompt:'请输入方案名称搜索',
        height:24,
        width:200,
        searcher:function(v,n){
           $('#table3').datagrid('load', {condition:v,type:1});
        }
    })
	
	//由 规则类型选项 联动显示 校验方法 的数据
	$('#methodTypes').combobox({
		width:200,
        valueField:'ids',    //选项值
        textField:"texts",   //文本值
		required:true,
        data:[{
            "ids":1,
            "texts":"格式校验",
        },{
            "ids":2,
            "texts":"空值校验"
        },{
            "ids":3,
            "texts":"长度及范围校验"
        },{
            "ids":4,
            "texts":"代码校验"
        }],
		onSelect:function(record){
			$.post(urls['getcheckmethodlist'], {ids : record.ids}, function(datas){
					$('#checkWays').combobox('loadData',datas);
					console.log(datas);
					if(datas.length == 1){
						$('#checkWays').combobox('clear');
						$('#checkWays').combobox('select',datas[0].texts); 
					}else if(datas.length == 0){
						$('#checkWays').combobox('clear');
					}else if(datas.length >= 2){
						$('#checkWays').combobox('clear');
						$('#checkWays').combobox('loadData',datas);
					}
			},'json');
		}
	})
	$('#checkWays').combobox({
		valueField:'ids',    //选项值
        textField:"texts",	//文本值
		onSelect:function(record){
			$.post(urls['getRuleParamList'], {ids : record.ids}, function(datas){
				console.log(datas);
				$('#checkRuleTable').datagrid("loadData",datas);
			});
		}
	})
	
	//设置严重程度下拉框的值
	$('#severity').combobox({
		valueField:'ids',    //选项值
        textField:"texts",   //文本值
		required:true,
        data:[{
            "ids":1,
            "texts":"正常",
        },{
            "ids":2,
            "texts":"轻微"
        },{
            "ids":3,
            "texts":"严重"
        }],
	});
})
// function initComboBox(start, length){
//     var list = [];
//     for(var i = 0; i < length; i++,start++){
//         list[i] = {};
//         list[i].value = "'" +start + "'";
//         list[i].text = start
//     }
//     return list;
// }

function func3(v,r,i){
	return  '<a data-hover="查看详情" title="查看详情" class="detail3" href="javascript:basDetail();" data-option=""></a>'
}

function checkBaseBtn(){
    var rows = $('#table3').datagrid('getSelections');
    if(rows.length == 0){
        $('#editBaseBtn,#delBaseBtn').linkbutton('disable')
    }else if(rows.length == 1){
        $('#editBaseBtn,#delBaseBtn').linkbutton('enable')
    }else{
        $('#editBaseBtn').linkbutton('disable');
        $('#delBaseBtn').linkbutton('enable');
    }
}

/*$(function () {
	$("#combobox_type221").combobox({
		width: 130,
		valueField: 'id',
		textField: "text",
		data: [{
			"id": 1,
			"text": "全部"
		}, {
			"id": 2,
			"text": "治安"
		}, {
			"id": 3,
			"text": "其他"
		}
		],
	})
})*/
/*$(function () {
	$("#combobox_type222").combobox({
		width: 130,
		valueField: 'id',
		textField: "text",
		data: [{
			"id": 1,
			"text": "全部"
		}, {
			"id": 2,
			"text": "人员基本信息库"
		}, {
			"id": 3,
			"text": "其他"
		}
		],
	})
})
$(function () {
	$("#combo_type008").combobox({
		width: 120,
		valueField: 'id',
		textField: "text",
		data: [{
			"id":  "全部",
			"text": "全部"
		}, {
			"id": 'card',
			"text": "card"
		}, {
			"id": "其他",
			"text": "其他"
		}
		],
	})
})
$(function () {
	$("#combo_type009").combobox({
		width: 120,
		valueField: 'id',
		textField: "text",
		data: [{
			"id":  "全部",
			"text": "全部"
		}, {
			"id": 'card',
			"text": "card"
		}, {
			"id": "其他",
			"text": "其他"
		}
		],
	})
})

$(function () {
	$("#combo_type010").combobox({
		width: 120,
		valueField: 'id',
		textField: "text",
		data: [{
			"id":  "固定时间",
			"text": "固定时间"
		}, {
			"id": '手动',
			"text": "手动"
		}, {
			"id": "其他",
			"text": "其他"
		}
		],
	})
})


$(function () {
    $("#toTable").datagrid({
        url: '/toTable/tolist',
    })
	$('#crlSearchBox').searchbox({
		prompt: '请输入资源名搜索',
		height: 24,
		width: 130,
		searcher: function (v, n) {
			$('#toTable').datagrid('load');
			console.log(v);
			console.log('111');
		}
	})
})
*/
//前台详情方法
function basDetail() {
	var row=$("#table3").datagrid('getSelections');
    linkbutton_click('open_dialog',{dialog:'#detDialog3'});
    $('.schemename').val(row[0].schemename);
    $('.card').val(row[0].card);
    $('.methodname').val(row[0].methodname);
    $('.dotime').val(row[0].dotime);

}
function bas() {
	var datas = $("#commonRuleTable").datagrid('getSelections');
	var dataid = datas[0].id;
	console.log(datas[0].id);
	
	$.post(urls['saveBasicTesting'], {data:dataid}, function(msg){
		$("#commonRuleDialog").dialog('close');
		$("#commonRuleTable").datagrid('reload');
	});
}

//前台新增
function addMonitorBase(index){
    initDialog('#baseDialog', '#table3', '新增');
	$('input[name="id"]').val('');
}
//前台删除方法
function basDel(i) {
	console.log(123);
	var data = getDelIDList(i, '#table3');
    if(data == false){
	  return	
	}
    $.messager.confirm('提示','是否删除选中记录', function(ok){
        if(ok){
            $.post(urls['deleteBasicTesting'], {ids:data}, function(msg){
                if(msg.errorCode != '0x0000'){
                    $.messager.alert('错误', msg.errorString, 'error')
                }else{
                    $('#table3').datagrid('reload')
                }
            })
        }
    })
}
//前台修改方法
function changeBas() {
	var row=$("#table3").datagrid('getSelections');
	if(row.length==0||row.length>1) {
		$.messager.confirm('警告', '请选择一条数据', 'warning');
	}
	else{
		linkbutton_click('open_dialog',{dialog:'#changeBas'});
		$('.schemenamechange').val(row[0].schemename);
		$('.checkobjectchange').val(row[0].checkobject);
		$('.schemetypechange').val(row[0].schemetype);
        $('.dotimechange').val(row[0].dotime);
		$('.idchange').val(row[0].id);
	}
}
/*function table3preserved() {
	$('#change_list3').form('submit', {
		url: "/table3/changeBas/",
		onSubmit: function () {
			return $(this).form('validate');
		},
		success: function (data) {
			$('#changeBas').dialog('close');
			$('#table3').datagrid('reload');
		}
	});
}

//下一步选项卡
$(function () {
//重置
	$('.reset').bind('click', function () {
		$('.objForm').form('reset')
	})
		})

	$('#xiss').bind('click', function () {
		$('#tb').tabs('add', {
			title: '填写基本信息',
			closable: true,
			href: '/table3/getContent/writeInfo',
		})
	})


		$('#next1').bind('click', function () {
        
			$('#tb').tabs('add', {
				title: '添加校验规则',
				closable: true,
				href:'/table3/getContent/addrule',
			})
		})
		$('#next2').bind('click', function () {
        
			$('#tb').tabs('add', {
				title: '选择展现字段',
				closable: true,
				href: '/table3/getContent/shofie',
			})
        
		})
		$('#next3').bind('click', function () {
        
			$('#tb').tabs('add', {
				title: '配置调度方案',
				closable: true,
				href: '/table3/getContent/way',
			})
        
        
		})



	$("#rules").datagrid({
		// url: '/tab/list3/',
		method: 'post',
		autoRowHeight: true,
		columns: [[
			{field: 'card', title: '校验字段', align: 'center', width: '15%',},
			{field: 'rulename', title: '规则名称', align: 'center', width: '15%',},
			{field: 'ruletype', title: '规则类型', align: 'center', width: '15%'},
			{field: 'methodname', title: '校验方法', align: 'center', width: '15%',},
			{field: 'serious', title: '严重程度', align: 'center', width: '15%',},
			{field: 'oper', title: '操作', align: 'center', width: '30%',},

		]],
	})*/

//前台增加方法
//function bb() {
// 	$("#bbForm").form('submit', {
// 		url: '/tab/list3/',
// 		onSubmit: function () {
// 					console.log(12)
//
// 			return true
// 		},
// 		success: function (data) {
// 			$("#bbDialog").dialog('close');
// 			$("#rules").datagrid('reload');
//
// 		}
// 	});
// }
	/*var isValid = $('#bbForm').form('validate');
    if(!isValid)
        return false;
    var data = $('#bbForm').serializeArray();
    var rows = $('#rules').datagrid('getData');
    var temp = {}
    for(var i in data){
        temp[data[i].name] = data[i].value
    }
	$('#rules').datagrid('appendRow', temp);
    $('#bbDialog').dialog('close');
    $('#rules').datagrid('clearSelections');
}

$(function () {
	$("#combobox_type666").combobox({
		width: 120,
		valueField: 'id',
		textField: "text",
		data: [{
			"id": "全部",
			"text": "全部"
		}, {
			"id":"身份证号码",
			"text": "身份证号码"
		}, {
			"id": "其他",
			"text": "其他"
		}
		],
	})
})

$(function () {
	$("#combobox_type667").combobox({
		width: 120,
		valueField: 'id',
		textField: "text",
		data: [{
			"id": "全部",
			"text": "全部"
		}, {
			"id": "长度校验",
			"text": "长度校验"
		}, {
			"id": "其他",
			"text": "其他"
		}
		],
	})
})
$(function () {
	$("#combobox_type668").combobox({
		width: 120,
		valueField: 'id',
		textField: "text",
		data: [{
			"id": "全部",
			"text": "全部"
		}, {
			"id":  "轻微",
			"text": "轻微"
		}, {
			"id": "其他",
			"text": "其他"
		}
		],
	})
})



$(function() {
	$("#problems2").datagrid({
		// url: '/tab/list3/',
		method: 'post',
		autoRowHeight: true,
		columns: [[
			{field: 'card', title: '校验字段', align: 'center', width: '50%',},
			{field: 'remark', title: '备注', align: 'center', width: '50%',},

		]],
	})
})

$(function() {
	$("#parameters2").datagrid({
		url: '/parameters/loadList/',
		autoRowHeight: true,
		columns: [[
			{field: 'parametername', title: '参数名', align: 'center', width: '10%',},
			{field: 'parameterchinese', title: '参数中文名', align: 'center', width: '10%',},
			{field: 'parametertype', title: '参数类型', align: 'center', width: '15%'},
			{field: 'datatype', title: '数据类型', align: 'center', width: '25%',},
			{field: 'defaultvalue', title: '默认值', align: 'center', width: '20%', },
		]],
	})
})
*/

//新增监测方案
function addMonitorBase() {
	//$('#baseDialog').dialog("open");
	initDialog('#baseDialog','#table3','新增监测方案');
    //initData(false,[]);
    var bar = $('#next_save').linkbutton('options').bar;
    /*$('#next_save').linkbutton('options').fromFieldAndToField = [];
    $('#next_save').linkbutton('options').ManyResourceData = [];
    $('#next_save').linkbutton('options').isEditor = true;
    $('input[name="resNum"]').eq(0).attr('checked',true)*/
    while($('#dataQualityTab').tabs('exists', 1)){
        $('#dataQualityTab').tabs({
            bar:{},
            onBeforeClose:function(){
                for(var i in bar){
                    if($(this).find('#'+ i).length != 0){
                        $(this).tabs('options').bar[i] = true;
                    }
                }
            },
            onClose:function(){
                var bars = $(this).tabs('options').bar;
               for(var i in bars){
                   if(bars[i] == true) {
                       $('body').append(bar[i]);
                       bars[i] = false;
                   }
               }
            }
        }).tabs('close', 1);
    }
}
function func(v,r,i){
	return  '<a class="detail" href="javascript:metDetail();" data-option="">编辑</a>'+'&nbsp;'+
			'<a class="detail111" href="javascript:metCheck();" data-option="">删除</a>'
}

//添加常用规则
function addCommonRule(){
	$('#commonRuleDialog').dialog('open');
	$('#commonRuleTable').datagrid({
		fit:true,
		pagination:false,
		singleSelect:true,
		method:'post',
		url:urls['getOftenRules'],
		columns: [[
			{field: 'checkbox', checkbox: true},
			{field: 'fieldName', title: '字段名', width: '15%'},
			{field: 'chineseName', title: '中文名称', width: '15%'},
			{field: 'nullRate', title: '空值率', width: '12%'},
			{field: 'identifier', title: '信息代码', width: '12%'},
			{field: 'standardDE', title: '标准数据元', width: '12%'},
			{field: 'checkNull', title: '空值校验', width: '8%'},
			{field: 'checkCode', title: '代码校验', width: '8%'},
			{field: 'checkStand', title: '标准校验', width: '8%'},
			/*{field: 'Object_words', title: '对象类词', width: '20%',
				formatter: function(value,row,index){
						return row.Object_words.cname;
				}},
			{field: 'Identifier', title: '标识符', width: '20%',
				formatter: function(value,row,index){
						return row.Identifier.fname;
				}},*/
		]],
	});
}

//添加校验规则
function addCheckRule(){
	$('#checkRuleDialog').dialog('open');
	$('#checkRuleTable').datagrid({
		fit:true,
		pagination:false,
		columns: [[
			{field: 'checkbox', checkbox: true},
			{field: 'paramName', title: '参数名', width: '20%'},
			{field: 'paramChiName', title: '参数中文名', width: '20%'},
			{field: 'dataType', title: '数据类型', width: '20%'},
			{field: 'isNull', title: '非空', width: '20%'},
			{field: 'paramValue', title: '参数值', width: '20%'},
		]],
	});
}

function initComboBox(start, length){
    var list = [];
    for(var i = 0; i < length; i++,start++){
        list[i] = {};
        list[i].value = start;
        list[i].text = String(start);
    }
    return list;
}

$(function(){
		$('#next_save').linkbutton({
        value:'next',
        clicks:0,
        html:[''],
        isEditor:true,
        lengths : $('.frequencySetting').length ,
        titles : ['添加校验规则','选择展现字段','配置调度方案'],
        fromFieldAndToField:[],
        tempRecord:{},
        ManyResourceData:[],
        height: $('#dataQualityTab').find('a.tabs-inner:eq(0)').height(),
       
        onClick:function(){
            var t = $(this),
                opt = t.linkbutton('options'),
                value = opt.value,
                html = opt.html,
                tabs = $('#dataQualityTab'),
                tab = tabs.tabs('getSelected'),
                index = tabs.tabs('getTabIndex',tab) + 1,
                length = opt.lengths,
                titles = opt.titles,
                height = opt.height;
            if(opt.clicks == 0) {
                for (var i =0; i<length; i++) {
                    var ht = $('.frequencySetting').eq(i).html();
                    html.push(ht)
                }
                opt.clicks++;
            }

            $('.frequencySetting').remove();
            if(value == 'next'){
                var validate_input =tab.find('.validatebox-invalid');
                if(validate_input.length != 0){
                    validate_input.eq(0).addClass('textbox-focused').focus().mouseover();
                    return false;
                }
                if(opt.isEditor == false){
                    $.messager.alert('错误','有正在编辑的行,请结束编辑','error');
                    return false;
                }
                if($('#dataQualityTab').tabs('exists',index)){
                    //console.log($('#dataQualityTab').tabs('getTab',index).panel('options'))
                    if($('#dataQualityTab').tabs('getTab',index).panel('options').disabled == true){
                        index = index + 1
                    }
                }
                if(!$('#dataQualityTab').tabs('exists',index)){
                    $('#dataQualityTab').tabs({
                        onAdd:function(){
                            var select_tab = tabs.tabs('getTab', index);
                            if($('span.combo').next('span.combo').length != 0){
                               $('span.combo').next('span.combo').remove()
                            }
			
                            $('#dataQualityTab').find('a.tabs-inner:gt(0)').css({height: height + 'px', 'line-height': height + 'px'})
                            //$('.dialog_table:eq('+index+')').find('td:eq(0)').width($('.dialog_table:eq(0)').find('td:eq(0)').width());
                            $('input[name="SchedulingPlan"]').change()
                            if(index == length){
                                opt.value = 'save'
                                t.linkbutton({text:'确定'})
                            }
                            var fromData = toData = '';

                            if(select_tab.find('#ManyResourceList').length != 0) {
                                $('#ManyResourceList').datagrid({
                                    fit:true,
                                    pagination:false,
                                    columns: [[
                                        {field: 'checkbox', checkbox: true},
                                        {field: 'CheckField', title: '校验字段', width: '17%'},
										{field: 'CheckRuleType', title: '规则名称', width: '17%'},
                                        {field: 'CheckRuleType', title: '规则类型', width: '17%'},
										{field: 'CheckMethod', title: '校验方法', width: '17%'},
                                        {field: 'Severity', title: '严重程度', width: '10%'},
										{field:'oper',title:'查看',align:'center',width:'10%',formatter:func},
                                    ]],
                                    
                                }).datagrid('loadData',opt.ManyResourceData)
                            }

                            if(select_tab.find('#fieldCheckList').length != 0) {
                                $('#fieldCheckList').datagrid({
                                    //toolbar: '#fieldCheckToolBar',
                                    fit:true,
                                    pagination:false,
                                    columns: [[
                                        {field: 'checkbox', checkbox: true},
                                        {field: 'FieldName', title: '字段名', width: '60%'},
                                        {field: 'fromTableField', title: '备注', width: '40%'},
                                    ]],
                                   
                                }) 
                            }
							
							if(select_tab.find('#fieldProjectList').length != 0) {
								$('#fieldProjectList').show();
							}
							$('input[name="timeType"]').change();
						},  
 
                        onSelect:function(title,i){
							
                            if(i == length){
                                opt.value = 'save';
                                t.linkbutton({text:'确定'});
                            }else{
                                opt.value = 'next';
                                t.linkbutton({text:'下一步'});
                            }
                        }
                    }).tabs('add', {
                        title:titles[index - 1],
                        content:html[index],
                    })
                }else{
                   $('#dataQualityTab').tabs('select',index);
                }

            }else if( value == 'save'){
                $('#addBaseForm').form('submit',{
                    url:urls['saveBasicTesting'],
                    onSubmit:function(){
                        return $(this).form('validate');
                    },
                    success:function () {
						while($('#dataQualityTab').tabs('exists',1)){
							$('#dataQualityTab').tabs('close',1);
						}
						resetContent();
						$('#addBaseForm').form('clear');
                        $('#baseDialog').dialog('close');
						$('#table3').datagrid('reload');
						t.linkbutton({text:'确定',disabled:false});
                    }
                })
            }
        },
    })
	
	
	$('#addBaseForm').delegate( 'input[name="timeType"]', 'change',function(){
        if($(this).is(":checked")){
			$('#days1').hide();
			$('#intervalDay1').hide();
			$('#once_time1').hide();
			var index = $(this).index()
		}
        switch (index){
            case 0:
                $('.month_day1,.play_time1').show();
                $('.week_day1').hide();
                $('#cycle1').next().show().end().combobox('enable').combobox('enableValidation');
                $('#once_time1').datetimebox('disableValidation').datetimebox('disable').next().hide();
                $('#hours1,#minutes1').next().show().end().combobox('enable').combobox('enableValidation');
                $('#intervalDay1,#days1').combobox('disableValidation').combobox('disable').next().hide();
                $('.words').hide();
                if( $('#cycle1').combobox('getValue') == 1 ){
                    $('#days1').next().show().end().combobox('enable').combobox('enableValidation');
                    $('.words:eq(0)').show();
					
                }else if($('#cycle1').combobox('getValue') == 2){
                    $('#days1').combobox('disableValidation').combobox('disable').next().hide();
                    $('.week_day1').show()
                    $('.words:eq(0)').hide();
					
                }else if($('#cycle1').combobox('getValue') == 3){
                    $('.words:eq(0)').hide();
                }else if($('#cycle1').combobox('getValue') == ''){
					$('#days1').css('display','none');
					$('#intervalDay1').css('display','none');
					$('#once_time1').css('display','none');
					$('.week_day1').css('display','none');
				}
				$('.month_day1').children(':eq(0)').html('执行周期:')
                break;
            case 1:
                $('.month_day1').show();
                $('#days1,#intervalDay1,#cycle1,#hours1,#minutes1').combobox('disableValidation').combobox('disable').next().hide();
                $('.words,.play_time1,.week_day1').hide();
                $('#once_time1').next().show().end().datetimebox('enable').datetimebox('enableValidation');
				$('.month_day1').children(':eq(0)').html('执行时间:');
                break;
            case 2:
                $('#cycle1,#days1,#intervalDay1,#hours1,#minutes1').combobox('disableValidation').combobox('disable');
                $('#once_time1').datetimebox('disableValidation').datetimebox('disable').next().hide();
                $('.month_day1,.week_day1').hide();
                $('.play_time1,.words').hide();
				$('.month_day1').children(':eq(0)').html('执行周期:');
                break;
            case 3:
                $('.month_day1,.play_time1').show();
                $('#intervalDay1,#hours1,#minutes1').next().show().end().combobox('enable').combobox('enableValidation');
                $('#once_time1').datetimebox('disableValidation').datetimebox('disable').next().hide();
                $('#cycle1,#days1').combobox('disableValidation').combobox('disable').next().hide();
                $('.words:eq(0),.week_day').hide();
                $('.words:eq(1)').show();
				$('.month_day1').children(':eq(0)').html('间隔时间:');
                break;
        }
    });
});

//表单提交成功后重置表单
function resetContent() {
    var clearForm = document.getElementById('addBaseForm');
    if (null != clearForm && typeof(clearForm) != "undefined") {
        clearForm.reset();
    }
}

function selectCycle(record){
    $(this).combobox('checkSelect');
    switch (record.value){
        case 1:
            $('#days1').next().show().end().combobox('enable').combobox('enableValidation');
            $('.words:eq(0)').show();
            $('.week_day1').hide();
            break;
        case 2:
            $('#days1').combobox('disableValidation').combobox('disable').next().hide();
            $('.week_day1').show();
            $('.words:eq(0)').hide();
            break;
        case 3:
            $('.week_day1').hide();
            $('#days1').combobox('disableValidation').combobox('disable').next().hide();
            $('.words:eq(0)').hide()
            break;
    }
}

function addBaseCancel(){
	$('#baseDialog').dialog('close');
	while($('#dataQualityTab').tabs('exists',1)){
		$('#dataQualityTab').tabs('close',1);
	}
}


