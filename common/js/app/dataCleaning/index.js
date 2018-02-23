function initComboBox(start, length){
    var list = [];
    for(var i = 0; i < length; i++,start++){
        list[i] = {};
        list[i].value = "'" +start + "'";
        list[i].text = String(start)
    }
    return list;
}

function getFromTable(){
      var datas = '';
        $.ajax({
            type:'post',
            async:false,
            //data:{tableName:tableName,dbName:dbName},
            dataType:'json',
            url:urls['getCollectTable'],
            success:function(msg){
                datas = msg
            }
        })
        return datas;
}

var fromTable = [],joinTable = {}
$(function(){
    $('input[name="resNum"]').change(function(){
        //alert($(this).val())
        if($(this).val() == 1){
            if($('#dataCleanTab').tabs('exists',1))
                $('#dataCleanTab').tabs('disableTab',1)
        }
        if($(this).val() == 2){
            if($('#dataCleanTab').tabs('exists',1))
                $('#dataCleanTab').tabs('enableTab',1)
        }
    })
    $('#cleaningForm').delegate( 'input[name="timeType"]', 'change',function(){
        if($(this).is(":checked"))
            var index = $(this).index()
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
                    $('.week_day').show()
                    $('.words:eq(0)').hide();
                }else if($('#cycle').combobox('getValue') == 3){
                    $('.words:eq(0)').hide();
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
                $('#once_time').datetimebox('disableValidation').datetimebox('disable').next().hide();
                 $('#cycle,#days').combobox('disableValidation').combobox('disable').next().hide();
                $('.words,.week_day').hide();
                $('.words:eq(1)').show();
                break;
        }
    });


    loadDataList({
        list: '#dataCleanList',
        toolbar: '#cleanEnableToolBar',
    });
    searchRules('#dataCleaningEnableSearch','#dataCleanList');

    $('#next_save').linkbutton({
        value:'next',
        clicks:0,
        html:[''],
        isEditor:true,
        lengths : $('.frequencySetting').length ,
        titles : ['多数据源配置','频率设定','字段映射','校验规则', '清洗规则'],
        fromFieldAndToField:[],
        tempRecord:{},
        ManyResourceData:[],
        height: $('#dataCleanTab').find('a.tabs-inner:eq(0)').height(),
        bar:{'ManyResourceToolBar':$('#ManyResourceToolBar').prop('outerHTML'),'fieldMapToolBar':$('#fieldMapToolBar').prop('outerHTML'),'fieldCheckToolBar':$('#fieldCheckToolBar').prop('outerHTML'),'fieldCleanToolBar':$('#fieldCleanToolBar').prop('outerHTML'),},
        onClick:function(){
            var t = $(this),
                opt = t.linkbutton('options'),
                value = opt.value,
                html = opt.html,
                tabs = $('#dataCleanTab'),
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
                if($('#dataCleanTab').tabs('exists',index)){
                    //console.log($('#dataCleanTab').tabs('getTab',index).panel('options'))
                    if($('#dataCleanTab').tabs('getTab',index).panel('options').disabled == true){
                        index = index + 1
                    }
                }
                if(!$('#dataCleanTab').tabs('exists',index)){
                    $('#dataCleanTab').tabs({
                        onAdd:function(){
                            var select_tab = tabs.tabs('getTab', index);
                            if($('span.combo').next('span.combo').length != 0){
                               $('span.combo').next('span.combo').remove()
                            }
                            $('#dataCleanTab').find('a.tabs-inner:gt(0)').css({height: height + 'px', 'line-height': height + 'px'})
                            //$('.dialog_table:eq('+index+')').find('td:eq(0)').width($('.dialog_table:eq(0)').find('td:eq(0)').width());
                            $('input[name="timeType"]').change()
                            if(index == length){
                                opt.value = 'save'
                                t.linkbutton({text:'确定'})
                            }
                            var fromData = toData = '';

                            if(select_tab.find('#ManyResourceList').length != 0) {
                                $('#ManyResourceList').datagrid({
                                    toolbar: '#ManyResourceToolBar',
                                    fit:true,
                                    pagination:false,
									striped:true,
                                    columns: [[
                                        {field: 'checkbox', checkbox: true},
                                        {field: 'fromTableName', title: '清洗数据源', width: '20%'},
                                        {field: 'fromTableField', title: '源表字段', width: '20%'},
                                        {field: 'joinTableName', title: '关联表', width: '20%', },
                                        {field: 'joinTableField', title: '关联表字段', width: '20%', },
                                        {field: 'oper', title: '操作', width: '15%', formatter: operationManyResource}
                                    ]],
                                    onLoadSuccess: function (data) {
                                        $('.edit').linkbutton({iconCls: 'icon-edit'});
                                        $('.del').linkbutton({iconCls: 'icon-cancel'});
                                    }
                                }).datagrid('loadData',opt.ManyResourceData)
                                searchRules('#ManyResourceSearch', '#ManyResourceList')
                               // console.log($('#ManyResourceList').datagrid('options'))
                                if($('input[name="resNum"]:checked').val() == 1){
                                    tabs.tabs('disableTab',index)
                                }
                            }

                            if(select_tab.find('#fieldCheckList').length != 0) {
                                $('#fieldCheckList').datagrid({
                                    toolbar: '#fieldCheckToolBar',
                                    fit:true,
                                    pagination:false,
									striped:true,
                                    columns: [[
                                        {field: 'checkbox', checkbox: true},
                                        {field: 'fromFieldName', title: '字段名', width: '25%'},
                                        {field: 'ruleID', title: '规则ID', width: '25%'},
                                        {field: 'ruleName', title: '规则名称', width: '25%', formatter:function(v, r, i){
                                            var checkRuleData = $('#fieldCheckForm input[comboname="ruleID"]').combobox('getData');
                                            for(var i=0; i < checkRuleData.length; i++){
                                                if (checkRuleData[i].id == r.ruleID){
                                                    return checkRuleData[i].name;
                                                }
                                            }
                                        }},
                                        {field: 'oper', title: '操作', width: '20%', formatter: operationFieldCheck}
                                    ]],
                                    onLoadSuccess: function (data) {
                                        $('.edit').linkbutton({iconCls: 'icon-edit'});
                                        $('.del').linkbutton({iconCls: 'icon-cancel'});
                                    }
                                })
                                searchRules('#fieldCheckSearch', '#fieldCheckList')
                            }
                            if(select_tab.find('#fieldCleanList').length != 0) {
                                $('#fieldCleanList').datagrid({
                                    toolbar: '#fieldCleanToolBar',
                                    fit:true,
                                    pagination:false,
									striped:true,
                                    columns: [[
                                        {field: 'checkbox', checkbox: true},
                                        {field: 'fromFieldName', title: '字段名', width: '25%'},
                                        {field: 'ruleID', title: '规则ID', width: '25%'},
                                        {field: 'ruleName', title: '规则名称', width: '25%', formatter:function(v, r, i){
                                            var cleanRuleData = $('#fieldCleanForm input[comboname="ruleID"]').combobox('getData');
                                            for(var i=0; i < cleanRuleData.length; i++){
                                                if (cleanRuleData[i].id == r.ruleID){
                                                    return cleanRuleData[i].name;
                                                }
                                            }
                                        }},
                                        {field: 'oper', title: '操作', width: '20%', formatter: operationFieldClean}
                                    ]],
                                    onLoadSuccess: function (data) {
                                        $('.edit').linkbutton({iconCls: 'icon-edit'});
                                        $('.del').linkbutton({iconCls: 'icon-cancel'});
                                    }

                                })
                                searchRules('#fieldCleanSearch', '#fieldCleanList')
                            }

                            if(select_tab.find('#fieldMapList').length != 0){
                                if(fromData == ''){
                                    var list = $('#ManyResourceList').datagrid('getRows');
                                    var tableName = $('#fromTableCombo').combobox('getValue');
                                    for(var i = 0; i< list.length; i++)
                                        tableName += ',' + list[i].fromTableName
                                    //if(tableName.indexOf(',') != -1)
                                     //   tableName = tableName.substr(0, tableName.length - 1)
                                    //console.log(list)
                                    fromData = getFieldsByTable(tableName , collectdb, true)
                                }
                                if(toData == ''){
                                    toData = getFieldsByTable($('#toTableCombo').combobox('getValue'), standarddb)
                                }

                                $('#fieldMapList').datagrid({
                                    toolbar: '#fieldMapToolBar',
                                    fit:true,
                                    pagination:false,
									striped:true,
                                    columns: [[
                                        {field: 'checkbox', checkbox: true},
                                        {field: 'fromFieldName', title: '汇集字段名', width: '25%',editor:{type:'combobox',options:{
                                                textField:'text',
                                                valueField:'value',
                                                groupField:'tableName',
                                                data:fromData,
                                                onSelect:function(record){
                                                    $(this).combobox('checkSelect');
                                                    opt.tempRecord = record;
                                                },
                                                onShowPanel:function(){
                                                    $(this).combobox('reloadData', fromData)
                                                    $(this).combobox('checkSelect')
                                                }
                                            }}},
                                        {field: 'fromTable', title: '所属表',hidden:true, width: '20%',},
										{field: 'chInfluxFieldName', title: '汇集字段中文名', width: '15%',showTitle:true,},
                                        {field: 'toFieldName', title: '标准字段名', width: '10%',},
										{field: 'chStandardFieldName', title: '标准字段中文名',width: '15%',},
										{field: 'identFieldName', title: '数据元标识符',showTitle:true, width: '10%',},
                                        {field: 'oper', title: '操作', width: '10%', formatter: operationFieldMap}
                                    ]],
                                    onLoadSuccess: function (data) {
                                        select_tab.find('.edit').linkbutton({iconCls: 'icon-edit'})
                                        select_tab.find('.del').linkbutton({iconCls: 'icon-cancel'})
                                    },
                                    onBeginEdit:function(index,row){
                                        //console.log('')
                                        select_tab.find('.edit:eq('+index+')').linkbutton({'iconCls':'icon-save'})
                                        select_tab.find('.del:eq('+index+')').linkbutton({'iconCls':'icon-cancel'})
                                        opt.isEditor = false;
                                    },
                                    onAfterEdit:function(index,row,changes){
                                        if(row.fromFieldName != '')
                                            $(this).datagrid('updateRow',{
                                                index:index,
                                                row:{
                                                    chInfluxFieldName:opt.tempRecord.name,
                                                    fromTable:opt.tempRecord.tableName
                                                }
                                            })
                                        select_tab.find('.edit:eq('+index+')').linkbutton({'iconCls':'icon-edit'})
                                        select_tab.find('.del:eq('+index+')').linkbutton({'iconCls':'icon-cancel'})
                                        opt.isEditor = true;
                                    }
                                }).datagrid('enableCellEditing');
                                var fromFieldAndToFieldObj = {};

                                //console.log(opt.fromFieldAndToField)
                                if(opt.fromFieldAndToField.length != 0) {
                                    var fromFieldAndToField = $.parseJSON(opt.fromFieldAndToField);
                                    for (var i in fromFieldAndToField) {
                                        fromFieldAndToFieldObj[fromFieldAndToField[i]] = i;
                                    }
                                }

                                for(var i in toData){
                                    var rows = $('#fieldMapList').datagrid('getData')
                                    var temp = {};
                                    //console.log(toData[i].value)
                                    //console.log(fromFieldAndToFieldObj[toData[i].value])
                                    if(fromFieldAndToFieldObj[toData[i].value] != undefined) {
                                        temp.fromFieldName = fromFieldAndToFieldObj[toData[i].value];
                                        for(var j = 0; j< fromData.length; j++){
                                            if(fromData[j].value == temp.fromFieldName){
                                                temp.chInfluxFieldName = fromData[j].name;
                                                break;
                                            }
                                        }
                                        //temp.chInfluxFieldName = fromData[i].name;
                                    }else {
                                         temp.fromFieldName = ''
                                    }
                                    //temp.fromTable = fieldFromTable[toData[i].value] == undefined ? '' : fieldFromTable[toData[i].value] ;
									//temp.chInfluxFieldName = fromData[i].name;
                                    temp.toFieldName = toData[i].value;
									temp.chStandardFieldName = toData[i].name;
									temp.identFieldName = toData[i].identFieldName;
                                    temp.oper = operationFieldMap('', temp, rows.total)
                                    //console.log(temp)
                                    $('#fieldMapList').datagrid('appendRow', temp);
                                    //if(toData[i].value == 'SAWPBH') return;
                                    select_tab.find('.edit').linkbutton({iconCls: 'icon-edit'})
                                    select_tab.find('.del').linkbutton({iconCls: 'icon-cancel'})
                                }
                                searchRules('#fieldMapSearch', '#fieldMapList');
                            }
                            if($('#dataCleanTab').tabs('exists',index)) {
                                if ($('#dataCleanTab').tabs('getTab', index).panel('options').disabled == true) {
                                    $('#next_save').click()
                                }
                            }
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
                   $('#dataCleanTab').tabs('select',index);
                }

            }else if( value == 'save'){
                $('#cleaningForm').form('submit',{
                    url: urls['saveUrl'],
                    onSubmit:function(param){
                        //将字典映射表格转成JSON格式传入后台
                        var data = $('#ManyResourceList').datagrid('getRows'),tables = [], condition = '';
                        if(data.length != 0) {
                            for (var i = 0; i < data.length; i++) {
                                tables.push(data[i].fromTableName)
                                tables.push(data[i].joinTableName)
                                condition += data[i].fromTableName + '.' + data[i].fromTableField + '=' + data[i].joinTableName + '.' + data[i].joinTableField + ','
                            }
                            if (condition != '')
                                condition = condition.substr(0, condition.length - 1)
                            var table = $.unique(tables)
                            param.joinTableFields = condition
                            param.fromTable = table.join(',');
                        }
                        param.fromFieldAndToField = getPostDataFromTable('fieldMapList', 'fromFieldName', 'toFieldName');

                        //param.fieldFromTable = getPostDataFromTable('fieldMapList', 'fromFieldName', 'fromTable');

                        //将字段对应校验规则表格转成JSON格式传入后台
                        param.fromFieldAndCheckRule = getPostDataFromTable('fieldCheckList', 'fromFieldName', 'ruleID');
                        //将字段对应转换规则表格转成JSON格式传入后台
                        param.fromFieldAndCleanRule = getPostDataFromTable('fieldCleanList', 'fromFieldName', 'ruleID');
                    },
                    success:function (res) {
                        res = $.parseJSON(res)
                        if(res.errorCode!='0x0000'){
                            $.messager.alert('错误', res.errorString, 'error');
                        }else{
                            $('#dataCleanList').datagrid('reload');
                            $('#cleaningDialog').dialog('close');
                        }
                    }
                })
            }
        },
    })
    fromTable =  getFromTable()
    $('#fromTableCombo,input[comboname="fromTableName"]').combobox('loadData', fromTable)
});

function getFieldsByTable(tableName,dbName, t){
    var datas = '';
    $.ajax({
        type:'post',
        async:false,
        data:{tableName:tableName,dbName:dbName, reTableName: t  == true ? 'yes': 'no'},
        dataType:'json',
        url:urls['getFieldsByTable'],
        success:function(msg){
            datas = msg
        }
    })
    return datas;
}

function getPostDataFromTable(tableId, firstField, secondField){
    var tableRows = $('#'+tableId).datagrid('getData').rows;
    var dataObj = new Object();
    for(var i in tableRows){
        if(tableRows[i][firstField] == ''){
            continue;
        }
        dataObj[tableRows[i][firstField]] = tableRows[i][secondField];
    }
    return JSON.stringify(dataObj).replace(/\\\\/g,'\\');
}

function getLoadDataFromData(data, firstField, secondField){
    var dataObj = $.parseJSON(data);
    var dataObjList = [];
    for(var key in dataObj){
        var tmp = new Object();
        tmp[firstField] = key;
        tmp[secondField] = dataObj[key];
        dataObjList.push(tmp);
    }
    return dataObjList
}

function selectCycle(record){
    $(this).combobox('checkSelect');
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


function loadDataList(obj){
    $(obj.list).datagrid({
        url:obj.url ,
        queryParams:{
            type: obj.type ? obj.type  : 0,
        },
        method:'post',
        toolbar:obj.toolbar,
        onSelect:checkButton,
        onSelectAll:checkButton,
        onUnselect:checkButton,
        onUnselectAll:checkButton,
		striped:true,
        columns:[[
            {field:'checkbox',checkbox:true},
            {field:'name',title:'任务名称',width:'13%'},
            {field:'flag',hidden:true, width:'10%'},
            {field:'flagShow',title:'启用状态',width:'10%', formatter:function (v, r, i) {
                if(r.flag){
                    return '启用'
                }else{
                    return '禁用'
                }
            }},
            {field:'status',hidden:true},
            {field:'statusShow',title:'执行状态',width:'10%', formatter: function (v, r, i) {
                if(r.status == 1){
                    return '正在执行'
                }else if(r.status == 2){
                    return '执行出错'
                }else{
                    return '空闲'
                }
            }},
            // {field:'timeType',title:'执行时间类型',width:'10%'},
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
            {field:'timeStrShow',title:'执行频率',width:'17%', formatter: function(v, r, i){
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
            {field:'description',title:'任务描述',width:'20%'},
            {field:'oper',title:'操作',width:'18%',formatter:operationCleaningRules},
        ]],
        onLoadSuccess:function(){
            $('.enableCleaning').linkbutton();
            $('.disableCleaning').linkbutton();
            $('.startCleaning').linkbutton();
            $('.editCleaning').linkbutton();
            $('.delCleaning').linkbutton();
            checkButton()
        },
    });
   // checkStatus(10000);
}


function checkStatus(time){
    if(typeof excutionStatus != 'undefined')
        clearInterval(excutionStatus)
    var excutionStatus = setInterval(function(){
        $('#dataCleanList').datagrid('reload')
    }, time)
}

function searchRules(search, list){
    $(search).searchbox({
        prompt:'请输入搜索条件',
        height:24,
        width:200,
        searcher:function(v,n){
            var url = $(list).datagrid('options').url;
            //console.log(v,n)
            if(url)
                $(list).datagrid('load', {condition:v})
            else {
                $(list).datagrid('checkRow', v);
                //console.log($(list).datagrid('getValueByField', 'fromFieldName'))
            }
        }
    })
}

function checkButton(){

}



function operationCleaningRules(value,row,index) {
    if(row.flag){
        return '<a class="easyui-linkbutton enableCleaning" onclick="endisableCleaning('+row.id+',\'enableUrl\')" data-options="iconCls:\'icon-ok\', disabled:true" title="启用" style="margin-right: 5px;"></a>' +
                '<a class="easyui-linkbutton disableCleaning" onclick="endisableCleaning('+row.id+',\'disableUrl\')" data-options="iconCls:\'icon-no\'" title="禁用" style="margin-right: 5px;"></a>' +
                '<a class="easyui-linkbutton startCleaning" onclick="startCleaning('+row.id+')" data-options="iconCls:\'icon-redo\'" title="立即执行" style="margin-right: 5px;"></a>' +
                '<a class="easyui-linkbutton editCleaning" onclick="editCleaning('+index+')" data-options="iconCls:\'icon-edit\', disabled:true" title="编辑" style="margin-right: 5px;"></a>' +
                '<a class="easyui-linkbutton delCleaning" onclick="delCleaning('+index+')" data-options="iconCls:\'icon-cancel\', disabled:true" title="删除" ></a>'
    }else{
        return '<a class="easyui-linkbutton enableCleaning" onclick="endisableCleaning('+row.id+',\'enableUrl\')" data-options="iconCls:\'icon-ok\'" title="启用" style="margin-right: 5px;"></a>' +
                '<a class="easyui-linkbutton disableCleaning" onclick="endisableCleaning('+row.id+',\'disableUrl\')" data-options="iconCls:\'icon-no\', disabled:true" title="禁用" style="margin-right: 5px;"></a>' +
                '<a class="easyui-linkbutton startCleaning" onclick="startCleaning('+row.id+')" data-options="iconCls:\'icon-redo\', disabled:true" title="立即执行" style="margin-right: 5px;"></a>' +
                '<a class="easyui-linkbutton editCleaning" onclick="editCleaning('+index+')" data-options="iconCls:\'icon-edit\'" title="编辑" style="margin-right: 5px;"></a>' +
                '<a class="easyui-linkbutton delCleaning" onclick="delCleaning('+index+')" data-options="iconCls:\'icon-cancel\'" title="删除" ></a>'
    }
}


function addCleaning(){
    initDialog('#cleaningDialog','#dataCleanList','增加清洗任务');
    //initData(false,[]);
    var bar = $('#next_save').linkbutton('options').bar;
    $('#next_save').linkbutton('options').fromFieldAndToField = [];
    $('#next_save').linkbutton('options').ManyResourceData = [];
    $('#next_save').linkbutton('options').isEditor = true;
    $('input[name="resNum"]').eq(0).attr('checked',true)
    while($('#dataCleanTab').tabs('exists', 1)){
        $('#dataCleanTab').tabs({
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

function editCleaning(i){
    var data = getEditData(i, '#dataCleanList');
    if(data == false)
        return false;
    initDialog('#cleaningDialog','#dataCleanList','修改清洗任务',data);
    // $('input[name="resNum"]').each(function(){
    //     if(data.fromTable.indexOf(',') != -1 && $(this).val() == 2){
    //         $(this).attr('checked',true)
    //     }else{
    //         $(this).attr('checked',false)
    //     }
    // })
    $('#next_save').linkbutton('options').fromFieldAndToField = data.fromFieldAndToField;
    $('#next_save').linkbutton('options').isEditor = true
    var bar = $('#next_save').linkbutton('options').bar;
    while($('#dataCleanTab').tabs('exists', 1)){
        $('#dataCleanTab').tabs({
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
    if(data.resNum == 2){
        var joinFields = data.joinTableFields.split(/[,\.=]/);
        list = []
        //console.log(joinFields)
        $('#fromTableCombo').combobox('select', joinFields[2])
        for(var i = 0; i < joinFields.length; i+=4){
            temp = {
                fromTableName:joinFields[i],
                fromTableField:joinFields[i+1],
                joinTableName:joinFields[i+2],
                joinTableField:joinFields[i+3],
            }
            list.push(temp)
        }
        $('#next_save').linkbutton('options').ManyResourceData = list;
    }
    var length = $('#next_save').linkbutton('options').lengths;
    for(var i = 0; i < length ; i++){
        $('#next_save').click();
        if(i == 1){
            $('input[name="timeType"]').each(function(){
                if($(this).val() == data.timeType){
                    $(this).attr('checked',true);
                    $(this).change()
                }
            })

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
        if(i==length-1){
            //$('#ManyResourceList').datagrid('loadData', list)
            //$('#fieldMapList').datagrid('loadData', getLoadDataFromData(data.fromFieldAndToField, 'fromFieldName', 'toFieldName'));
            $('#fieldCheckList').datagrid('loadData', getLoadDataFromData(data.fromFieldAndCheckRule, 'fromFieldName', 'ruleID'));
            $('#fieldCleanList').datagrid('loadData', getLoadDataFromData(data.fromFieldAndCleanRule, 'fromFieldName', 'ruleID'));
        }
    }

}

function delCleaning(i){
    var ids = getDelIDList(i, '#dataCleanList');
    if(ids){
        $.messager.confirm('确认', "确认要删除该任务？操作不可还原！", function (r) {
            if(r){
                saveDel(urls['deleteUrl'], '#dataCleanList', ids);
            }
        });
    }
}

function endisableCleaning(id, url) {
    $.post(urls[url], {id: id}, function (msg) {
        if (msg.errorCode != '0x0000') {
            $.messager.alert('错误', msg.errorString, 'error');
        }else {
            $.messager.alert('成功', msg.errorString, 'success');
            $('#dataCleanList').datagrid('reload');
        }
    }, 'json');
}

function startCleaning(id){
    $.post(urls['startUrl'], {id: id}, function (msg) {
        if (msg.errorCode != '0x0000') {
            $.messager.alert('错误', msg.errorString, 'error');
        }else {
            $.messager.alert('成功', msg.errorString, 'success');
            $('#dataCleanList').datagrid('reload');
        }
    }, 'json');
}

function operationFieldCheck(v, r, i){
    return '<a  onclick="editFieldCheck('+i+')" class="edit" title="编辑"  style="margin-right: 5px;"></a>' +
            '<a  onclick="delFieldCheck('+i+')" class="del" title="删除" ></a>'
}

function operationFieldMap(v, r, i){
    return '<a  onclick="editFieldMap('+i+')" class="edit" title="编辑"  style="margin-right: 5px;"></a>' +
            '<a  onclick="delFieldMap('+i+')" class="del" title="删除" ></a>'
}


function operationFieldClean(v, r, i){
    return '<a  onclick="editFieldClean('+i+')" class="edit" title="编辑"  style="margin-right: 5px;"></a>' +
            '<a  onclick="delFieldClean('+i+')" class="del" title="删除" ></a>'
}

function operationManyResource(v, r, i){
    return '<a  onclick="editManyResource('+i+')" class="edit" title="编辑"  style="margin-right: 5px;"></a>' +
            '<a  onclick="delManyResource('+i+')" class="del" title="删除" ></a>'
}


function addFieldCheck(){
    initDialog('#fieldCheckDialog','#fieldCheckList','增加校验规则');
    reloadFromFieldName('#fieldMapList', '#fieldCheckForm', 'fromFieldName')
    $('input[name="fieldCheckAction"]').val('add');
}

function reloadFromFieldName(list, form, field){
    var rows = $(list).datagrid('getValueByField', field);
    //var data = $(form).find('input[comboname="fromFieldName"]').combobox('getData');
	var list = $('#ManyResourceList').datagrid('getRows');
	var tableName = $('#fromTableCombo').combobox('getValue');
	for(var i = 0; i< list.length; i++)
		tableName += ',' + list[i].fromTableName
	//if(tableName.indexOf(',') != -1)
	 //   tableName = tableName.substr(0, tableName.length - 1)
	//console.log(list)
	console.log(tableName)
	var data = getFieldsByTable(tableName , collectdb, true)
	console.log(data)
    var new_data = []
    for(var i in data)
        if($.inArray(data[i].value, rows) != -1)
          new_data.push(data[i])
    $(form).find('input[comboname="fromFieldName"]').combobox('loadData',new_data).combobox('checkSelect')
}

function editFieldCheck(i){
    var data = getEditData(i, '#fieldCheckList');
    if(data == false)
        return false;
    initDialog('#fieldCheckDialog','#fieldCheckList','修改校验规则', data);
    if(i != undefined)
        $('#fieldCheckForm input[name="fieldCheckAction"]').val('edit' + i);
    else
        $('#fieldCheckForm input[name="fieldCheckAction"]').val('edit');
    reloadFromFieldName('#fieldMapList', '#fieldCheckForm', 'fromFieldName');
}

function delFieldCheck(i){
    var ids = [];
    if(i != undefined){
        ids.push(i)
    }else{
        var list = $('#fieldCheckList').datagrid('getSelections');
        if(list.length == 0){
            $.messager.alert('错误',"请至少选择一条数据删除",'error');
            return false
        }
        for(var j in list){
            ids.unshift($('#fieldCheckList').datagrid('getRowIndex',list[j]))
        }
    }
    $.messager.confirm('确定提示框','是否确定删除选中记录？',function(ok){
        if(ok){
            for(var i in ids){
                $('#fieldCheckList').datagrid('deleteRow',ids[i])
            }
        }
    })
}


function addFieldClean(){
    initDialog('#fieldCleanDialog','#fieldCleanList','增加字典转换');
    reloadFromFieldName('#fieldMapList', '#fieldCleanForm', 'fromFieldName')
    $('input[name="fieldCleanAction"]').val('add');
}

function editFieldClean(i){
    var data = getEditData(i, '#fieldCleanList');
    if(data == false)
        return false;
    initDialog('#fieldCleanDialog','#fieldCleanList','修改字典转换', data);
    if(i != undefined)
        $('#fieldCleanForm input[name="fieldCleanAction"]').val('edit' + i);
    else
        $('#fieldCleanForm input[name="fieldCleanAction"]').val('edit');
    reloadFromFieldName('#fieldMapList', '#fieldCleanForm', 'fromFieldName');
}

function delFieldClean(i){
    var ids = [];
    if(i != undefined){
        ids.push(i)
    }else{
        var list = $('#fieldCleanList').datagrid('getSelections');
        if(list.length == 0){
            $.messager.alert('错误',"请至少选择一条数据删除",'error');
            return false
        }
        for(var j in list){
            ids.unshift($('#fieldCleanList').datagrid('getRowIndex',list[j]))
        }
    }
    $.messager.confirm('确定提示框','是否确定删除选中记录？',function(ok){
        if(ok){
            for(var i in ids){
                $('#fieldCleanList').datagrid('deleteRow',ids[i])
            }
        }
    })
}

function initJoinTableName(){
    var data = []
    for(var i in joinTable)
        data.push(joinTable[i])
    return data
}

function editFieldMap(i){
    var data = $('#fieldMapList').datagrid('getRows')[i]
    var value = '';
    if(data.fromFieldName != ''){
        value = data.fromFieldName.split('.')[1]
    }
    $('#fieldMapList').datagrid('editCell', {index:i, field:'fromFieldName',value: value});
}

function delFieldMap(i){
     var ids = [];
    if(i != undefined){
        ids.push(i)
    }else{
        var list = $('#fieldMapList').datagrid('getSelections');
        if(list.length == 0){
            $.messager.alert('错误',"请至少选择一条数据删除",'error');
            return false
        }
        for(var j in list){
            ids.unshift($('#fieldMapList').datagrid('getRowIndex',list[j]))
        }
    }
    $.messager.confirm('确定提示框','是否确定删除选中记录？',function(ok){
        if(ok){
            for(var i in ids){
                $('#fieldMapList').datagrid('deleteRow',ids[i])
            }
        }
    })
}

function addManyResource(){
    $('input[comboname="joinTableName"]').combobox('loadData', initJoinTableName())
    $('input[comboname="joinTableField"]').combobox('loadData', [])
    $('input[comboname="formTableField"]').combobox('loadData', [])
    initDialog('#ManyResourceDialog','#ManyResourceList','增加字段映射');
    $('input[name="ManyResourceAction"]').val('add');
}


function editManyResource(i){
    //$('#ManyResource').datagrid('editCell', {index:i, field:'fromFieldName',value: data.fromFieldName});
    //console.log($('#fieldMapList').datagrid('beginEdit', i).datagrid('getEditors'))
    var data = getEditData(i, '#ManyResourceList');
    if(data == false)
        return false;
    $('input[comboname="joinTableName"]').combobox('loadData', initJoinTableName())
    $('input[comboname="joinTableField"]').combobox('loadData', [])
    $('input[comboname="formTableField"]').combobox('loadData', [])
    initDialog('#ManyResourceDialog','#ManyResourceList','修改字段映射', data);
    if(i != undefined)
        $('input[name="ManyResourceAction"]').val('edit' + i);
    else
        $('input[name="ManyResourceAction"]').val('edit');
}

function delManyResource(i){
    var ids = [];
    if(i != undefined){
        ids.push(i)
    }else{
        var list = $('#ManyResourceList').datagrid('getSelections');
        if(list.length == 0){
            $.messager.alert('错误',"请至少选择一条数据删除",'error');
            return false
        }
        for(var j in list){
            ids.unshift($('#ManyResourceList').datagrid('getRowIndex',list[j]))
        }
    }
    $.messager.confirm('确定提示框','是否确定删除选中记录？',function(ok){
        if(ok){
            for(var i in ids){
                $('#ManyResourceList').datagrid('deleteRow',ids[i])
            }
        }
    })
}


function saveDel(url, list, ids){
    $.post(url, {data:ids}, function(msg){
        if(msg.errorCode != '0x0000'){
            $.messager.alert('错误',msg.errorString,'error');
        }else{
            $.messager.alert('成功',msg.errorString,'success');
            $(list).datagrid('reload');
        }
    }, 'json')
}

function getDelIDList(i, listID){
    if(i != undefined){
        var data = $(listID).datagrid('getRows')[i],list = [];
        list.push(data)
    }else{
       var list = $(listID).datagrid('getSelections');
        if(list.length == 0){
            $.messager.alert('错误',"请至少选择一条数据删除",'error');
            return false
        }
    }
    ids = '';
    for(var i in list){
        if(list[i].flag == '1'){
            $.messager.alert('错误',"不能删除已启用的任务",'error');
            return false;
        }
        ids += list[i].id + ','
    }
    ids = ids.substr(0, ids.length - 1);
    return ids;
}


function getEditData(i, listID){
    if(i != undefined){
        var data = $(listID).datagrid('getRows')[i]
    }else{
        var list = $(listID).datagrid('getSelections');
        if(list.length == 0){
            $.messager.alert('错误',"请至少选择一条数据修改",'error');
            return false;
        }else if(list.length > 1){
            $.messager.alert('错误',"一次只能修改一条数据",'error');
            return false;
        }else{
            var data =  $(listID).datagrid('getSelected');
        }
    }

    return data;
}


function addManyResourceToGrid(){
    var isValid = $('#ManyResourceForm').form('validate');
    if(!isValid)
        return false;
    var data = $('#ManyResourceForm').serializeArray();
    var rows = $('#ManyResourceList').datagrid('getData');
    var fromTableInput = $('input[comboname="fromTableName"]'),fromTableData = fromTableInput.combobox('getData'),fromTableNameValue = fromTableInput.combobox('getValue')
    for(var i in fromTableData){
        if(fromTableData[i].value == fromTableNameValue) {
            joinTable[fromTableData[i].value] = fromTableData[i]
            break
        }
    }
    var temp = {}
    for(var i in data){
        temp[data[i].name] = data[i].value
    }
    /*
    for(var i in rows.rows){
        if(temp.toFieldName == rows.rows[i].toFieldName) {
            $.messager.alert('错误','该标准字段已经被映射','error');
            return false;
        }
    }*/
    if($('input[name="ManyResourceAction"]').val() == 'add') {
        temp.oper = operationManyResource('', temp, rows.total)
        $('#ManyResourceList').datagrid('appendRow', temp);
    }else{
        if($('#ManyResourceList').datagrid('getSelected') == null)
            var index = Number($('input[name="fieldCheckAction"]').val().substr(4))
        else
            var index = $('#ManyResourceList').datagrid('getRowIndex', $('#ManyResourceList').datagrid('getSelected'))
        $('#ManyResourceList').datagrid('updateRow',{
            index:index,
            row:temp,
        })
    }
    $('.edit').linkbutton({iconCls: 'icon-edit'})
    $('.del').linkbutton({iconCls: 'icon-cancel'})
    $('#ManyResourceDialog').dialog('close');
    $('#ManyResourceList').datagrid('clearSelections');
}


function addFieldCheckToGrid(){
    var isValid = $('#fieldCheckForm').form('validate');
    if(!isValid)
        return false;
    var data = $('#fieldCheckForm').serializeArray();
    var rows = $('#fieldCheckList').datagrid('getData');
    var temp = {}
    for(var i in data){
        temp[data[i].name] = data[i].value
    }

    if($('input[name="fieldCheckAction"]').val() == 'add') {
        for(var i in rows.rows){
            if(temp.fromFieldName == rows.rows[i].fromFieldName) {
                $.messager.alert('错误','该采集字段已经被映射','error')
                return false;
            }
        }
        temp.oper = operationFieldCheck('', temp, rows.total);
        $('#fieldCheckList').datagrid('appendRow', temp);
    }else{
        if($('#fieldCheckList').datagrid('getSelected') == null)
            var index = Number($('input[name="fieldCheckAction"]').val().substr(4))
        else
            var index = $('#fieldCheckList').datagrid('getRowIndex', $('#fieldCheckList').datagrid('getSelected'))
        $('#fieldCheckList').datagrid('updateRow',{
            index:index,
            row:temp,
        }).datagrid('clearSelections');
    }
    $('.edit').linkbutton({iconCls: 'icon-edit'});
    $('.del').linkbutton({iconCls: 'icon-cancel'});
    $('#fieldCheckDialog').dialog('close');
    $('#fieldCheckList').datagrid('clearSelections');
}

function addFieldCleanToGrid(){
    var isValid = $('#fieldCleanForm').form('validate');
    if(!isValid)
        return false;
    var data = $('#fieldCleanForm').serializeArray();
    var rows = $('#fieldCleanList').datagrid('getData');
    var temp = {}
    for(var i in data){
        temp[data[i].name] = data[i].value
    }

    if($('input[name="fieldCleanAction"]').val() == 'add') {
        for(var i in rows.rows){
            if(temp.fromFieldName == rows.rows[i].fromFieldName) {
                $.messager.alert('错误','该采集字段已经被映射','error')
                return false;
            }
        }
        temp.oper = operationFieldClean('', temp, rows.total);
        $('#fieldCleanList').datagrid('appendRow', temp);
    }else{
        if($('#fieldCleanList').datagrid('getSelected') == null)
            var index = Number($('input[name="fieldCheckAction"]').val().substr(4))
        else
            var index = $('#fieldCleanList').datagrid('getRowIndex', $('#fieldCleanList').datagrid('getSelected'))
        $('#fieldCleanList').datagrid('updateRow',{
            index:index,
            row:temp,
        }).datagrid('clearSelections');
    }
    $('.edit').linkbutton({iconCls: 'icon-edit'});
    $('.del').linkbutton({iconCls: 'icon-cancel'});
    $('#fieldCleanDialog').dialog('close');
    $('#fieldCleanList').datagrid('clearSelections');
}