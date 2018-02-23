function initComboBox(start, length){
    var list = [];
    for(var i = 0; i < length; i++,start++){
        list[i] = {};
        list[i].value = "'" +start + "'";
        list[i].text = String(start)
    }
    return list;
}
var html = new Array();

$(function(){
    //采集大类
	var taskType;
	for (var i =0; i < $('.frequencySetting').length; i++) {
		var ht = $('.frequencySetting').eq(i).prop('outerHTML');
		html.push(ht);
		//console.log(html);
    }
	$('.frequencySetting').remove();
    $('#collectTaskTypeCombobox').combobox({
        valueField: 'value',
		textField: 'text',
		data: [{
			"value": "1",
			"text": "文件类（包含XML，CSV等）"
		}, {
			"value": "2",
			"text": "数据库类"
		}, {
			"value": "3",
			"text": "Web Service"
		}],
        onSelect: function (record) {
            $(this).combobox('checkSelect')
			if(record.value == 1){
				taskType = 0;
				
			}else if(record.value == 2){
				taskType = 1;
				
			}else if(record.value == 3){
				taskType = 2;
				
			}
			//console.log(record.value);
			while($('#collectTaskTab').tabs('exists', 1)){
				$('#collectTaskTab').tabs('close', 1);
			}
        },
        onChange:function(){
            $(this).combobox('checkSelect')
        }
    });

    //采集数据库类细分
    

    $("#belongInstitutionCombobox").combobox({
        url: urls['getBelongInstitution'],
        textField:'recognname',
        valueField:'recognid',
    });
    $("#belongTypeCombobox").combobox({
        url: urls['getBelongType'],
        textField:'dataid',
        valueField:'dataname',
    });

    $("#collectTaskList").datagrid({
        url: urls['getCollectTaskListData'],
        autoRowHeight:true,
        columns:[[
            {field:'checkbox',checkbox:true},
            {field:'taskName',title:'任务名称',width:'20%',},
            {field:'taskType',title:'任务类型',width:'10%',
                formatter: function(value, row, index){
                    switch (value){
                        case 1:
                            return '文本类型'
                        case 2:
                            return '数据库类型'
                        case 3:
                            return 'Web Service'
                        default:
                            return value
                    }
                }
            },
            {field:'timeType',title:'执行时间类型',width:'10%', formatter: function (v, r, i) {
                if(r.timeType == 1){
                    return '固定时间'
                }else if(r.timeType == 2){
                    return '一次性'
                }else if(r.timeType == 3){
                    return '手动'
                }else {
                    return '间隔'
                }
            }},
            {field:'timeStr',hidden:true},
            {field:'timeStrShow',title:'执行频率',width:'15%', formatter: function(v, r, i){
                var time = $.parseJSON(r.timeStr);
                switch (r.timeType){
                    case 1:
                        if(time.day_of_week != '*') {
                            return '每星期' + time.day_of_week +'的'+ time.hour +'点'+ time.minute + '分';
                        }else if(time.day_of_month != '*'){
                            return '每月' + time.day_of_month + '号的' + time.hour +'点'+ time.minute + '分';
                        }else{
                            return '每天' + time.hour +'点'+ time.minute + '分';
                        }
                        break;
                    case 2:
                        return time.year + '-' + time.month_of_year + '-'+ time.day_of_month +' '+ time.hour +':'+ (time.minute == 0 ? '00' : time.minute);
                        break;
                    case 3:
                        return '手动';
                        break;
                    case 4:
                        var day_of_month = time.day_of_month;
                        if(day_of_month == '*'){
                            day_of_month = '0'
                        } else {
                            day_of_month = day_of_month.substring(2, day_of_month.length);
                        }
                        var hour = time.hour;
                        if(hour == '*'){
                            hour = '0'
                        } else {
                            hour = hour.substring(2, hour.length);
                        }
                        var minute = time.minute;
                        if(minute == '*'){
                            minute = '0'
                        } else {
                            minute = minute.substring(2, minute.length)
                        }
                        return '每隔' + day_of_month + '天' + hour + '时' + minute + '分';
                        break;
                    default:
                        $.messager.alert('错误', '调度计划类型错误',error);
                        return '错误';
                }

            }},
			
            {field:'taskStatus',title:'当前任务状态',width:'10%',
                formatter: function(value, row, index){
                    if (value==0){
                        return '未运行';
                    }
                    if (value==1)
                    {
                        return '正在采集';
                    }
                    if (value==2)
                    {
                        return '采集出错';
                    }
                }
            },
			{field:'taskProgress',title:'当前任务进度',width:'15%',formatter:sliderFun},
            {field:'oper',title:'操作',width:'20%',formatter:stateFunc},
        ]],
        queryParams: {
            collectNodeId: collectNodeId
        },
        onLoadSuccess: function(){
            // 图标
            $('.stateStop').linkbutton({iconCls: 'icon-no'});
            $('.stateStart').linkbutton({iconCls: 'icon-ok'});
            $('.runNow').linkbutton({iconCls: 'icon-tip'});
            $('.detailLog').linkbutton({iconCls: 'icon-search'});
			$('.progress').progressbar({});
            stateButton()
        },
    });

    //停用 启用 立即执行
    function stateFunc(v, r, i){
        str = ''
        if(r.flag == '1' ){
            str = '<a title="停用" class="stateStop" href="javascript:;" onclick="stateStop(\''+r.id+'\')" data-options=" " style="margin:8px 5px;"></a>'+
                '<a title="启用" class="stateStart" href="javascript:;" data-options="disabled:true" style="margin:8px 5px;"></a>'+
                '<a title="立即执行" class="runNow" href="javascript:;" onclick="runNow(\''+r.id+'\','+i+')" data-options="" style="margin:8px 5px;"></a>'
        } else {
            str = '<a title="停用" class="stateStop" href="javascript:;" data-options="disabled:true" style="margin:8px 5px;"></a>'+
                '<a title="启用" class="stateStart" href="javascript:;" onclick="stateStart(\''+r.id+'\')" data-options="" style="margin:8px 5px;"></a>'+
                '<a title="立即执行" class="runNow" href="javascript:;" onclick="runNow(\''+r.id+'\','+i+')" data-options="disabled:true" style="margin:8px 5px;"></a>'
        }
        str += '<a title="采集日志" class="detailLog" onclick="collectTaskLogDetail('+i+')"></a>'
        return str;
    }
	
	function sliderFun(v, r, i){
		
		console.log(r.taskStatus);
		/*if(r.taskStatus == 0){
			str = '<div class="progress" id="textValue" style="" data-options=""></div>';
		}else if(r.taskStatus == 1){
			str = '<div class="progress" id="textValue" style="" data-options=""></div>';
		}else if(r.taskStatus == 2){
			str = '<div class="progress" id="textValue" style="" data-options=""></div>';
		}*/
		var str = '<div class="progress textValue" id="" style="" data-options=""></div>';
		return str;
	}
	//从后台获取进度值函数
	function txtValue(v, r, i){
		var rows = $('#collectTaskList').datagrid('getSelections');
		console.log(rows);
		if(rows.length != 0){
			for(var i = 0;i < rows.length; i++){
				var ID = rows[i].id;
				console.log(ID);
				$.post(urls['getProgressBar'], {ids:ID}, function (data) {
					console.log(data);
					console.log(data.ids);
					if(data.taskProgress >= 100 || data.taskProgress == 0){
					window.clearInterval(timerId);
					}
					console.log(data.taskProgress);
					if(ID == data.ids){
						$('.textValue').progressbar('setValue',data.taskProgress);
					}
					
				}, 'json');
			}
		}
		

		/*$.ajax({
		    type:"post",
		    url:urls['getProgressBar'],
		    timeout:10000,//超时时间
		    dataType:"json",
			queryParams:{
                ids:rows[0].id
            },
		    success:function(msg){
			    console.log(msg);
			    if(msg.taskProgress >= 100 || msg.taskProgress == 0){
				 window.clearInterval(timerId);
			    }
			    $('#textValue').progressbar('setValue',msg.taskProgress);
		    },
		    //请求出错的处理
		    error:function(){
			    window.clearInterval(timerId);
			    alert("请求出错");
		    }
	   });*/
	}
	$(function(){
		timerId = window.setInterval(txtValue,3000);
	});
    function stateButton(){
        var dataAll = $('#collectTaskList').datagrid('getSelected');
    }

    $('#taskSearchBox').searchbox({
        prompt:'请输入任务名称搜索',
        height:24,
        width:200,
        searcher:function(v,n){
        $('#collectTaskList').datagrid('load', {condition:v,type:1});
        }
    });
	
	//选取不同的采集源类型  点击’下一步'的操作逻辑
    $('#next_save').linkbutton({
        value:'next',
        clicks:0,
        height: $('#collectTaskTab').find('a.tabs-inner:eq(0)').height(),
        titles: [],
        tableIds: [],
        isCheckPath:false,
        isEditor:true,
        fileFieldList:[],
        getFile:false,
        onClick: function () {
            var t = $(this),
                opt = t.linkbutton('options'),
                value = opt.value,
                tabs = $('#collectTaskTab'),
                tab = tabs.tabs('getSelected'),
                index = tabs.tabs('getTabIndex',tab) + 1,
                titles = opt.titles,
                tableIds = opt.tableIds,
                height = opt.height;
            var collectTaskType = $('#collectTaskTypeCombobox').combobox('getValue');

            if(collectTaskType){
                switch (collectTaskType){
                    case "1":
                        titles = ['文件配置','选择表', '频率设定'];
                        tableIds = ['#collectTaskFileTypeTable', '#collectTaskAddPreviewTable', '#collectTaskTimeScheduleTable'];
						
                        break;
                    case "2":
                        titles = ['数据库配置','选择表','频率设定'];
                        tableIds = ['#collectTaskDataBaseTypeTable', '#collectTaskAddPreviewTable','#collectTaskTimeScheduleTable'];
						
                        break;
                    case "3":
                        titles = ['服务配置','选择表', '频率设定'];
                        tableIds = ['#collectTaskWebServiceTable', '#collectTaskAddPreviewTable', '#collectTaskTimeScheduleTable'];
						
                        break;
                    default:
                        return false;
                }
            } else {
                return false;
            };
			
            if(opt.clicks == 0) {
                opt.clicks++;
            };

			//点击下一步的操作逻辑
            if(value == 'next'){
                var validate_input =tab.find('.validatebox-invalid');
                if(validate_input.length != 0){
                    validate_input.eq(0).addClass('textbox-focused').focus().mouseover();
                    return false;
                }
                 if(opt.isEditor == false){
                    $.messager.alert('错误','有正在编辑的行或列', 'error');
                    return false;
                }
                if(opt.isCheckPath == false && tab.find('#testServer').length != 0){
                    $.messager.alert('警告','请点击"测试连接"检测路径是否可用', 'warning')
                    return false;
                }

                if(!tabs.tabs('exists',index)){
                    tabs.tabs({
						onAdd:function(){
                            var select_tab = tabs.tabs('getTab', index);
							if($('span.combo').next('span.combo').length != 0){
                               $('span.combo').next('span.combo').remove();
                            }
                            if($('span.textbox').next('span.textbox').length != 0){
                               $('span.textbox').next('span.textbox').remove();
                            }
                            if(select_tab.find('#databaseTableName').length != 0){
                                var formArray = $('#collectTaskForm').serializeArray(),
                                    formObj = new Object();
                                for(var i = 0; i < formArray.length; i++){
                                    formObj[formArray[i].name] = formArray[i].value
                                }
                                select_tab.find('#databaseTableName').combobox({
                                    required:true,
                                    url:urls['getDataBaseTables'],
                                    queryParams: formObj,
                                    onHidePanel:function(){

                                    },
                                    keyHandler:{
                                        enter:function(e){
                                            var name = $(this).combobox('getText')
                                            if(name.split('.').length <=1){
                                                $.messager.alert('错误','表名有误，请检查!','error')
                                                return false;
                                            }
                                            if(e.keyCode){
                                                $('#collectTaskForm').form('submit', {
                                                    url: urls['getSelectAllSQL'],
                                                    onSubmit: function (param) {
                                                        param.databaseTableName = name
                                                        return true;
                                                    },
                                                    success: function (msg) {
                                                        $('#databaseCollectSQL').textbox('setValue', msg)
                                                    }
                                                });
                                            }
                                            $(this).combobox('hidePanel')
                                        },
                                        query:function(q,e){

                                        }
                                    },
                                    onSelect: function(record){
                                        $(this).combobox('checkSelect')
                                        if(record.value){
                                            $('#collectTaskForm').form('submit', {
                                                url: urls['getSelectAllSQL'],
                                                onSubmit: function () {
                                                    return true;
                                                },
                                                success: function (msg) {
                                                    $('#databaseCollectSQL').textbox('setValue', msg)
                                                }
                                            });
                                        }
                                    }
                                })

                            }
                            if(select_tab.find('#fieldLimitCode').length != 0){
                                $('#fieldLimitCode').combobox({
                                    valueField:'value',
                                    textField:'text',
                                    data:[{
                                        text:'"',
                                        value:'"',
                                    },{
                                        text:"'",
                                        value:"'"
                                    },{
                                        text:'无',
                                        value:'no'
                                    }]
                                }).combobox('select', '"')
                            }
                            if(select_tab.find('#fieldSplitCode').length != 0){
                                $('#fieldSplitCode').combobox({
                                    valueField:'value',
                                    textField:'text',
                                    data:[{
                                        text:'定位',
                                        value:'\\t',
                                    },{
                                        text:"分号(;)",
                                        value:";"
                                    },{
                                        text:'逗号(,)',
                                        value:','
                                    },{
                                        text:'空格',
                                        value:'\\s',
                                    },{
                                        text:'其他符号',
                                        value:'other',
                                    },],
                                    onSelect:function(record){
                                        $(this).combobox('checkSelect')
                                        if(record == undefined){
                                            $(this).combobox('setValue','')
                                            return
                                        }
                                        if(record.value == 'other'){
                                            $('<input class="easyui-validatebox textbox" style="width:40px;height:20px;margin-left: 5px;" name="otherSplitCode" data-options="required:true,validType:\'length[1,1]\'" />').insertAfter($(this).next());
                                            $('input[name="otherSplitCode"]').validatebox()
                                       }else
                                            if($('input[name="otherSplitCode"]').length != 0)
                                                $('input[name="otherSplitCode"]').remove()
                                    }
                                }).combobox('select', '\\t')
                                checkLimitAndSplit(select_tab, $('#collectTaskFileTypeCombobox').combobox('getValue'))
                                $('#collectTaskFileTypeCombobox').combobox({
                                    onSelect:function(record){
                                        $(this).combobox('checkSelect')
                                        checkLimitAndSplit(select_tab, record.value)
                                    }
                                })
                            }
                            if(select_tab.find('#fileField').length != 0){
                                var fileField = [];
                                var obj = getServerData();
                                var rowFieldVlaue = ''
                                if(obj.fileType == 'xml'){
                                    $('#rowField').parents('tr').show().end().combobox()
                                    $('#fileRoot').parents('tr').show().end().combobox({
                                        queryParams:obj,
                                        textField:'text',
                                        valueField:'value',
                                        onSelect:function(record){
                                            $(this).combobox('checkSelect')
                                            obj.fileRoot = record.value
                                            obj.rootPath = record.text
                                            $('#rowField').combobox({
                                                queryParams:obj,
                                                textField:'text',
                                                valueField:'value',
                                                onSelect:function(r){
                                                    console.log(11111111111111)
                                                    $(this).combobox('checkSelect')
                                                    if(opt.fileFieldList.length == 0) {
                                                        $('#fileField').datagrid('options').url = urls['getDataGridList']
                                                        var obj = getServerData();
                                                        try{
                                                            obj.rootPath = r.value
                                                        }catch(e) {
                                                            obj.rootPath = ''
                                                        }

                                                        $('#fileField').datagrid('load', obj)
                                                    }
                                                    else {
                                                        $('#fileField').datagrid({
                                                            data: opt.fileFieldList,
                                                        })
                                                        $('#fileField').datagrid('options').url = urls['getDataGridList']
                                                        opt.fileFieldList = []
                                                    }
                                                }
                                            }).combobox('select',rowFieldVlaue)
                                            if(rowFieldVlaue != ''){
                                                $('#rowField').combobox('disable')
                                            }
                                        },
                                        onLoadSuccess:function(){
                                            var value = $(this).combobox('getValue')
                                            rowFieldVlaue = $('#rowField').combobox('getValue')
                                            $(this).combobox('unselect',value).combobox('select', value)
                                        }
                                    })
                                }else if(obj.fileType != 'xml'){
                                    $('#rowField,#fileRoot').removeAttr('data-options').combobox().combobox('disable').parents('tr').hide();
                                    if(opt.fileFieldList.length == 0)
                                        $('#fileField').datagrid({queryParams:obj,fit:false})
                                    else
                                        $('#fileField').datagrid({
                                            data: opt.fileFieldList,
                                            fit:false,
                                        })
                                }
                                    $('#fileField').datagrid({
                                    pagination:false,
                                    url: opt.fileFieldList.length == 0 ? urls['getDataGridList'] : null,
                                    fit:false,
                                    singleSelect:true,
                                    columns:[[
                                        {field:'elementName',title:obj.fileType == 'xml' ? '标签名' : (obj.fileType == 'csv' ||  obj.fileType == 'txt'? '头名称' : ''),width:'15%',},
                                        {field:'fieldName',title:'字段名',width:'15%',editor:{type:'validatebox'}},
                                        {field:'fieldChineseName',title:'字段中文名',width:'15%',editor:{type:'validatebox'}},
                                        {field:'fieldType',title:'字段类型',width:'15%',editor:{type:'validatebox'}},
                                        {field:'fieldLength',title:'字段长度',width:'13%',editor:{type:'validatebox'}},
                                        {field:'preKey',title:'主键',width:'13%',editor:{type:'combobox',options:{
                                            valueField:'value',
                                            textField:'text',
                                            data:[{
                                                value:'YES',
                                                text:'是'
                                            },{
                                                value:'NO',
                                                text:'否'
                                            },]
                                        }}},
                                        {field:'oper',title:'操作',width:'15%',formatter:opt.fileFieldList.length == 0 ? operFileField : undefined},
                                    ]],
                                    onLoadSuccess: function (data) {

                                        select_tab.find('.edit').linkbutton({iconCls: 'icon-edit'});
                                        select_tab.find('.del').linkbutton({iconCls: 'icon-cancel'});
                                    },
                                    onBeginEdit:function(index,row){
                                        select_tab.find('.edit:eq('+index+')').linkbutton({'iconCls':'icon-save'});
                                        select_tab.find('.del:eq('+index+')').linkbutton({'iconCls':'icon-cancel'});
                                        opt.isEditor = false;
                                    },
                                    onAfterEdit:function(index,row,changes){
                                        select_tab.find('.edit:eq('+index+')').linkbutton({'iconCls':'icon-edit'});
                                        select_tab.find('.del:eq('+index+')').linkbutton({'iconCls':'icon-cancel'});
                                        opt.isEditor = true;
                                    }
                                })
                                if(opt.fileFieldList.length != 0){
                                    $('#fileRoot').combobox('disable')
                                }else{
                                    if(obj.fileType == 'xml')
                                        $('#fileRoot,#rowField').combobox('enable')
                                    $('#fileField').datagrid('enableCellEditing')
                                }


                                //if($('#filePath').val() != '' && $('#fileRoot').combobox('getValue') != ''){
                                    // if(opt.getFile == false){
                                    //     $.messager.alert('错误', '文件路径或者根目录有误，请确认', 'error');
                                    //     return false;
                                    // }
                                    // $('#fileField').datagrid('load', {path:$('#filePath').val(),rootPath:$('#fileRoot').combobox('getValue')})
                                //}
                            }
                            $('input[name="timeType"]').change();
						},
                        onSelect: function(title,i){
                            if(i == titles.length){
                                opt.value = 'save';
                                t.linkbutton({text:'确定'});
								
                            }else{
                                opt.value = 'next';
                                t.linkbutton({text:'下一步'});
                            }
                        }
                    }).tabs('add', {
                        title:titles[index - 1],
						content:$(html[taskType]).find(tableIds[index - 1]),
                    })
					
                } else {
                    tabs.tabs('select',index);
                }

            } else if( value == 'save') {
                $('#collectTaskForm').form('submit',{
                    url: urls['saveCollectTask'],
                    onSubmit: function(param){
                        var value = $('input[comboname="taskType"]').combobox('getValue')
                        if(value == 1){
                            var data = getServerData();
                            param.fileRoot = $('#fileRoot').combobox('getValue');
                            param.rowField = $('#rowField').combobox('getValue');
                            var fieldList = $('#fileField').datagrid('getData').rows;
                            for(var i in data)
                                param[i] = data[i]
                            param.fileFields = JSON.stringify(fieldList)
                        }else if(value == 2){
                            param.databaseCollectSQL = $('#databaseCollectSQL').textbox('getValue');
                            param.databaseTableName = $('#databaseTableName').combobox('getValue') == '' ? $('#databaseTableName').combobox('getText'): $('#databaseTableName').combobox('getValue')
                            param.databasePreviewNum = $('#databasePreviewNum').numberbox('getValue');
                        }
                        return $(this).form('validate');
                    },
                    queryParams:{
                        collectNodeId: collectNodeId
                    },
                    success: function (msg) {
                        msg = $.parseJSON(msg);
                        if(msg.errorCode == '0x0000'){
                            $.messager.alert('成功', msg.errorString, 'info');
                            $('#collectTaskDialog').dialog('close');
                            $('#collectTaskList').datagrid('reload');
							$('#collectTaskForm').form('clear');
							$('#collectTaskFileTypeTable').form('reset');
							
                        } else {
                            $.messager.alert('失败', msg.errorString, 'error');
                        }
                    }
                });
            }
        },
    });
	
	$('#collectTaskForm').delegate( 'input[name="timeType"]', 'change',function(){
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
                }else if($('#cycle').combobox('getValue') == 2){
                    $('#days').combobox('disableValidation').combobox('disable').next().hide();
                    $('.week_day').show();
                    $('.words:eq(0)').hide();
                }else if($('#cycle').combobox('getValue') == 3){
                    $('.words:eq(0)').hide();
                }else if($('#cycle').combobox('getValue') == ''){
					$('#days').css('display','none');
					$('#intervalDay').css('display','none');
					$('#once_time').css('display','none');
					$('.week_day').css('display','none');
				}
                $('.month_day').children(':eq(0)').html('执行周期:')
                break;
            case 1:
                $('.month_day').show();
                $('#days,#intervalDay,#cycle,#hours,#minutes').combobox('disableValidation').combobox('disable').next().hide();
                $('.words,.play_time,.week_day').hide();
                $('#once_time').next().show().end().datetimebox('enable').datetimebox('enableValidation');
                $('.month_day').children(':eq(0)').html('执行时间:')
                break;
            case 2:
                $('#cycle,#days,#intervalDay,#hours,#minutes').combobox('disableValidation').combobox('disable');
                $('#once_time').datetimebox('disableValidation').datetimebox('disable').next().hide();
                $('.month_day,.week_day').hide();
                $('.play_time,.words').hide();
                $('.month_day').children(':eq(0)').html('执行周期:')
                break;
            case 3:
                $('.month_day,.play_time').show();
                $('#intervalDay,#hours,#minutes').next().show().end().combobox('enable').combobox('enableValidation');
                $('#once_time').datetimebox('disableValidation').datetimebox('disable').next().hide();
                $('#cycle,#days').combobox('disableValidation').combobox('disable').next().hide();
                $('.words,.week_day').hide();
                $('.words:eq(1)').show();
                $('.month_day').children(':eq(0)').html('间隔时间:')
                break;
        }
    });

   // checkStatus(10000)
});


function checkStatus(time){
    if(typeof excutionStatus != 'undefined')
        clearInterval(excutionStatus)
    var excutionStatus = setInterval(function(){
        $('#collectTaskList').datagrid('reload')
    }, time)
}

function checkLimitAndSplit(tab, v){
    if(v == 'txt'){
        tab.find('#fieldLimitCode').combobox('enable').parents('tr').show();
        tab.find('#fieldSplitCode').combobox('enable').parents('tr').show();
    }else{
        if(tab.find('input[name="otherSplitCode"]').length != 0){
            tab.find('input[name="otherSplitCode"]').remove();
        }
        if(v == 'csv'){
            tab.find('#fieldLimitCode').combobox('enable').parents('tr').show();
            tab.find('#fieldSplitCode').combobox('disable').parents('tr').hide();
        }else{
            tab.find('#fieldLimitCode').combobox('disable').parents('tr').hide();
            tab.find('#fieldSplitCode').combobox('disable').parents('tr').hide();
        }
    }
}

function testServer(){
    //alert(1)
    var url = $('#collectTaskFileTypeTable').attr('action'),
        data = getServerData(),
        method = $('#collectTaskFileTypeTable').attr('method');
    $.post(url, data, function (msg) {
        if(msg.errorCode != '0x0000'){
            $.messager.alert('错误', msg.errorString, 'error')
            $('#next_save').linkbutton('options').isCheckPath = false
        }else{
            $.messager.alert('提示', msg.errorString, 'info')
           $('#next_save').linkbutton('options').isCheckPath = true
        }
    }, 'json')

}

function getServerData() {
    var data = $('#collectTaskFileTypeTable').serializeArray(),
    obj = {};
    for(var i in data){
        obj[data[i].name] = data[i].value
    }
    return obj;
}

function operFileField(value,row, index){
    var s = '<a class="edit" title="编辑" style="margin-right: 8px" onclick="editFileField('+index+')"></a>'
    var type = $('#collectTaskFileTypeCombobox').combobox('getValue')
    if(type == 'xml')
        s += '<a class="del" title="删除" onclick="delFileField('+index+')" ></a>'
    return s;
}

function editFileField(index){
    if(index == undefined){
        $.messager.alert('错误', '编辑的行不存在', 'error');
        return false;
    }
    var data = $('#fileField').datagrid('getRows')[index]
    var value = data.fieldName || '';
    if($('#next_save').linkbutton('options').isEditor == true)
        $('#fileField').datagrid('editCell', {index:index, field:'fieldName',value: value});
}

function delFileField(index){
    if(index == undefined){
        $.messager.alert('错误', '删除的行不存在', 'error');
        return false;
    }
    $('#fileField').datagrid('deleteRow', index)
}

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

//测试数据库连接
function testDataBaseConnect(){
    $('#collectTaskForm').form('submit',{
        url: urls['testDataBaseConnect'],
        onSubmit: function () {
            return true;
        },
        success: function (msg) {
            msg = $.parseJSON(msg)
            if(msg.errorCode == '0x0000'){
                $.messager.alert('成功', msg.errorString, 'info');
            } else {
                $.messager.alert('失败', msg.errorString, 'error');
            }
        }
    })
}

//停用
function stateStop(dataid){
	$.post(urls['endisableCollectTask'],{data:dataid},function(msg){
        if (msg.errorCode == '0x0000'){
            $.messager.alert('成功', '禁用成功', 'info');
        } else {
            $.messager.alert('失败', '禁用失败', 'error');
        }
		$("#collectTaskList").datagrid('reload');
	}, 'json')
}
// 启用
function stateStart(dataid){
	$.post(urls['endisableCollectTask'],{data:dataid},function(msg){
        if (msg.errorCode == '0x0000'){
            $.messager.alert('成功', '启用成功', 'info');
        } else {
            $.messager.alert('失败', '启用失败', 'error');
        }
		$("#collectTaskList").datagrid('reload');
	}, 'json')
}
//立即执行
var timerId;
function runNow(dataid,index,txtValue){
    $.post(urls['runCollectTask'], {data:dataid}, function (msg) {
        if (msg.errorCode == '0x0000'){
            $.messager.alert('成功', msg.errorString, 'info');
            $("#collectTaskList").datagrid('reload');
			//$("#collectTaskList").datagrid('refreshRow',index);
        } else {
            $.messager.alert('失败', msg.errorString, 'error');
        }
    }, 'json');
	//每隔3秒自动调用方法，实现进度条的实时更新
	//timerId = window.setInterval(txtValue,3000);
}

function addCollectTask() {
    $('#collectTaskDialog').dialog({
        title:'新增采集任务',
        onOpen:function(){
            $('#collectTaskForm').form('reset');
        },
        onClose:function(){
            $('#collectTaskList').datagrid('clearSelections')
        }
    }).dialog('open');
    $('#next_save').linkbutton('options').isCheckPath = false;
    $('#next_save').linkbutton('options').fileFieldList = [];
    $('#next_save').linkbutton('options').isEditor = true
    while($('#collectTaskTab').tabs('exists', 1)){
        $('#collectTaskTab').tabs('close', 1);
    }
}

function delCollectTask() {
	var data = $("#collectTaskList").datagrid('getSelections');
	if(data.length == 0){
		$.messager.alert('警告','请至少选择一条数据','warning');
		// return false;
	}
	else {
		$.messager.confirm('确认删除框', '是否确定删除选中记录?', function (ok) {
			if (ok) {
				var ids = '';
				for (var i in data) {
                    if (data[i].flag == '1'){
                        $.messager.alert('错误','不能删除已启用的任务','error');
                        return ;
                    }
					ids += data[i].id + ',';
				}
				ids = ids.substr(0, ids.length - 1);
				$.post(urls['delCollectTask'], {data: ids}, function (msg) {
                    if(msg.errorCode == '0x0000') {
                        $.messager.alert('成功', msg.errorString, 'info');
                    } else {
                        $.messager.alert('失败', msg.errorString, 'error');
                    }
					$("#collectTaskList").datagrid('reload');
				}, 'json')
			}
		})
	}
}

function editCollectTask() {
    var data = $('#collectTaskList').datagrid('getSelections');
    if(data.length!=1) {
		$.messager.alert('警告', '请选择一条数据', 'warning');
	} else {
        data = data[0];
        console.log(data);
        if(data.flag){
            $.messager.alert('错误', '任务已启用，无法编辑', 'error');
            return;
        }
        initDialog('#collectTaskDialog','#collectTaskList','修改采集任务',data);
        while($('#collectTaskTab').tabs('exists', 1)){
            $('#collectTaskTab').tabs('close', 1);
        }
        var titles, tableIds;
        var collectTaskType = $('#collectTaskTypeCombobox').combobox('getValue');

        if(collectTaskType){
            switch (collectTaskType){
                case "1":
                    titles = ['文件配置','选择表', '频率设定'];
                    tableIds = ['#collectTaskFileTypeTable', '#collectTaskAddPreviewTable', '#collectTaskTimeScheduleTable'];

                    break;
                case "2":
                    titles = ['数据库配置','选择表','频率设定'];
                    tableIds = ['#collectTaskDataBaseTypeTable', '#collectTaskAddPreviewTable','#collectTaskTimeScheduleTable'];

                    break;
                case "3":
                    titles = ['服务配置','选择表', '频率设定'];
                    tableIds = ['#collectTaskWebServiceTable', '#collectTaskAddPreviewTable', '#collectTaskTimeScheduleTable'];

                    break;
                default:
                    return false;
            }
        } else {
            return false;
        };
        $('#next_save').linkbutton('options').isCheckPath = true
        $('#next_save').linkbutton('options').isEditor = true
        if(data.taskType == 1){
            $('#next_save').linkbutton('options').fileFieldList = $.parseJSON(data.fileFields)
            //$('#fileField').datagrid('loadData', {total:fileFields.length, rows:fileFields});
        }
        for(var i = 0; i < titles.length ; i++){
            $('#next_save').click();
            initData(true, '#collectTaskDialog', data)
            if(i == titles.length - 1){
                $('input[name="timeType"]').each(function(){
                    if($(this).val() == data.timeType){
                        $(this).attr('checked',true);
                        $(this).change()
                    }
                });

                var time = $.parseJSON(data.timeStr);

                switch (data.timeType){
                    case 1:
                        if(time.day_of_week != '*') {
                            $('#cycle').combobox('select', 2);
                            $('input[name="week_day"]').each(function(){
                                if($.inArray($(this).val(), time.day_of_week) != -1)
                                    $(this).attr('checked',true);
                            })
                            $('#hours').combobox('select',time.hour);
                            $('#minutes').combobox('select',time.minute);
                        }else if(time.day_of_month != '*'){
                            $('#cycle').combobox('select', 1);
                            $('#days').combobox('select',time.day_of_month);
                            $('#hours').combobox('select',time.hour);
                            $('#minutes').combobox('select',time.minute);

                        }else{
                            $('#cycle').combobox('select', 3);
                            $('#hours').combobox('select',time.hour);
                            $('#minutes').combobox('select',time.minute);
                        }
                        break;
                    case 2:
                        var value = time.month + '/'+ time.day_of_month + '/'+time.year+' '+ time.hour +':'+time.minute;
                        $('#once_time').datetimebox('setValue', value);
                        break;
                    case 3:
                        break;
                    case 4:
                        var day_of_month = time.day_of_month;
                        if(day_of_month == '*'){
                            day_of_month = '0'
                        } else {
                            day_of_month = day_of_month.substring(2, day_of_month.length);
                        }
                        var hour = time.hour;
                        if(hour == '*'){
                            hour = '0'
                        } else {
                            hour = hour.substring(2, hour);
                        }
                        var minute = time.minute;
                        if(minute == '*'){
                            minute = '0'
                        } else {
                            minute = minute.substring(2, minute.length)
                        }
                        $('#intervalDay').combobox('select', day_of_month);
                        $('#hours').combobox('select', hour);
                        $('#minutes').combobox('select', minute);
                        break;
                    default:
                        $.messager.alert('错误', '调度计划类型错误',error);
                        return false;
                }
            }
        }
    }
}

function collectTaskLogDetail(i) {
    var id = ids = nodeId ='' ;
    if(i == undefined){
        var rows = $('#collectTaskList').datagrid('getSelections')
        if(rows.length == 1){
            id = rows[0].id
        }else if(rows.length > 1){
            for(var i in rows){
                ids += rows[i].id + ','
            }
            ids = ids.substr(0, ids.length - 1)
        }else{
            var data = $('#collectTaskList').datagrid('getData')
            if(data.total == 0){
                var path = location.pathname
                var array = path.split('/')
                nodeId = array[array.length - 2]
            }else{
                nodeId = data.rows[0].collectNodeId
            }
        }
    }else{
        id = $('#collectTaskList').datagrid('getData').rows[i].id
    }
    $('#collectTaskLogDialog').dialog({
        title: id != '' ? '任务日志详情' : (ids != '' ? '部分任务日志详情' : '节点任务日志详情'),
        onOpen:function(){
            $('#collectTaskLogList').datagrid({
                queryParams:{
                    id:id,
                    ids:ids,
                    nodeId:nodeId,
                },
                url:urls['getCollectTaskLog'],
                columns:[[
                    {field:'startTime',title:'任务开始时间',width:'25%'},
                    {field:'endTime',title:'任务结束时间',width:'25%'},
                    {field:'allCount',title:'采集总条数',width:'18%'},
                    {field:'successCount',title:'成功条数',width:'18%',formatter:function(value, row, index){
                        if(row.successCount != row.allCount){
                            return '<span style="display:block;width:100%;height:100%;background:red">'+value+'</span>';
                        }else
                            return value;
                    }},
                    {field:'taskStatus',title:'任务状态',width:'14%',formatter: function(value, row, index){
                    if (value==0){
                        return '未运行';
                    }
                    if (value==1)
                    {
                        return '正在采集';
                    }
                    if (value==2)
                    {
                        return '采集出错';
                    }
                }},
                ]]
            })
        }
    }).dialog('open')

}

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

//点击预览选项卡的 预览按钮  弹出的dataGrid  dialog
function previewDialog(){

    if($('#databaseCollectSQL').textbox('getValue') == ''){
        $.messager.alert('错误', '无可预览数据！', 'error');
        return false;
    }

    var databaseCollectSQL = $('#databaseCollectSQL').textbox('getValue');
    var fieldStr = databaseCollectSQL.match(/SELECT([\s\S]*)FROM/)[1];
    if(!fieldStr){
        $.messager.alert('错误', '请检查SQL语句！', 'error');
        return false;
    }
    // 根据sql语句获取字段
    fieldStr = fieldStr.replace(/[\s+\r\n\"]/g, '');
    var fieldArray = fieldStr.split(',');
    var columns = new Array();
    for (x in fieldArray){
        columns.push({
            field : fieldArray[x],
            title : fieldArray[x],
            width : 100,
            align : 'center'
        })
    }
    // form提交获取数据
    $('#collectTaskForm').form('submit', {
        url: urls['getPreviewData'],
        queryParams:{
            databaseCollectSQL: $('#databaseCollectSQL').textbox('getValue'),
            databasePreviewNum: $('#databasePreviewNum').numberbox('getValue'),
            fieldStr: fieldStr,
        },
        onSubmit: function () {
            return true;
        },
        success: function (msg) {
            msg = $.parseJSON(msg);
            if(msg.hasOwnProperty('errorCode')){
                $.messager.alert('错误', msg.errorString, 'error');
                return;
            }
            $('#addPreviewData').css('display','block');
            $('#collectTaskDataPanel').dialog({
                title : '预览',
                modal : true,
                width : fieldArray.length * 100,
                height : 500,
                zIndex : 10000,
                pagination: false,
                closable : true,
                collapsible : true,
                minimizable : true,
                maximizable : true,
                onOpen : function(){
                    var maxWidth = Number($('body').width() * 80 / 100)
                    $(this).css('max-width', maxWidth).prev().css('max-width', maxWidth).parents('.window').css('max-width', maxWidth).next().css('max-width', maxWidth)
                    var width = $('body').width()
                    if(fieldArray.length * 100 > width){
                        var mwidth = (fieldArray.length * 100 - width)/2 + (width-maxWidth) / 2
                        $(this).parents('.window').css('margin-left', mwidth).next().css('margin-left',mwidth)
                    }
                    $('#collectTaskDataGrid').datagrid({
                        columns : [columns],
                        data: msg
                    });
                },
                onClose : function() {
                    $('#collectTaskDataPanel').css('display','none');
                },
            }).dialog('open');
        }
    });
}
