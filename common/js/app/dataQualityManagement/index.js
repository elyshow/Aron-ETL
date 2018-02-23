/**
 * Created by Administrator on 2016-08-16.
 */
function initComboBox(start, length){
    var list = [];
    for(var i = 0; i < length; i++,start++){
        list[i] = {};
        list[i].value = "'" +start + "'";
        list[i].text = start
    }
    return list;
}
$(function(){
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
                if( $('#cycle').combobox('getValue') == 1 ){
                    $('#days').next().show().end().combobox('enable').combobox('enableValidation');
                }else if($('#cycle').combobox('getValue') == 2){
                    $('#days').combobox('disableValidation').combobox('disable').next().hide();
                    $('.week_day').show()
                }
                $('.words').hide();
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
                break;
        }
    });

    //
    // loadDataList({
    //     list: '#table3',
    //     toolbar: '#cleanEnableToolBar',
    // });
    // searchRules('#dataCleaningEnableSearch','#table3');

    $('#next_save').linkbutton({
        value:'next',
        clicks:0,
        html:[''],
        lengths : $('.frequencySetting').length ,
        titles : ['频率设定','字段映射','校验规则', '字典转换'],
        height: $('#dataCleanTab').find('a.tabs-inner:eq(0)').height(),
        bar:{'fieldMapToolBar':$('#fieldMapToolBar').prop('outerHTML'),'fieldCheckToolBar':$('#fieldCheckToolBar').prop('outerHTML'),'fieldCleanToolBar':$('#fieldCleanToolBar').prop('outerHTML'),},
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
                            if(select_tab.find('#fieldCheckList').length != 0) {

                                $('#fieldCheckList').datagrid({
                                    toolbar: '#fieldCheckToolBar',
                                    fit:true,
                                    columns: [[
                                        {field: 'checkbox', checkbox: true},
                                        {field: 'fromFieldName', title: '字段名', width: '30%'},
                                        {field: 'ruleID', title: '规则', width: '40%'},
                                        {field: 'oper', title: '操作', width: '14%', formatter: operationFieldCheck}
                                    ]],
                                    onLoadSuccess: function (data) {
                                        $('.edit').linkbutton({iconCls: 'icon-edit'});
                                        $('.del').linkbutton({iconCls: 'icon-cancel'});
                                    }

                                })
                                searchRules('#fieldCheckSearch', '#fieldCheckList')
                            }
                            if(select_tab.find('#fieldCleanList').length != 0) {
                                console.log(2)
                                $('#fieldCleanList').datagrid({
                                    toolbar: '#fieldCleanToolBar',
                                    fit:true,
                                    columns: [[
                                        {field: 'checkbox', checkbox: true},
                                        {field: 'fromFieldName', title: '字段名', width: '30%'},
                                        {field: 'ruleID', title: '规则', width: '40%'},
                                        {field: 'oper', title: '操作', width: '14%', formatter: operationFieldClean}
                                    ]],
                                    onLoadSuccess: function (data) {
                                        $('.edit').linkbutton({iconCls: 'icon-edit'});
                                        $('.del').linkbutton({iconCls: 'icon-cancel'});
                                    }

                                })
                                searchRules('#fieldCleanSearch', '#fieldCleanList')
                            }

                            if(select_tab.find('#fieldMapList').length != 0){

                                $('#fieldMapList').datagrid({
                                    toolbar: '#fieldMapToolBar',
                                    fit:true,
                                    columns: [[
                                        {field: 'checkbox', checkbox: true},
                                        {field: 'fromFieldName', title: '汇集字段名', width: '20%'},
                                        {field: 'toFieldName', title: '标准字段名', width: '20%'},
                                        {field: 'oper', title: '操作', width: '14%', formatter: operationFieldMap}
                                    ]],
                                    onLoadSuccess: function (data) {
                                        $('.edit').linkbutton({iconCls: 'icon-edit'})
                                        $('.del').linkbutton({iconCls: 'icon-cancel'})
                                    }

                                });
                                searchRules('#fieldMapSearch', '#fieldMapList');
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
                        param.fromFieldAndToField = getPostDataFromTable('fieldMapList', 'fromFieldName', 'toFieldName');
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
                            $('#table3').datagrid('reload');
                            $('#cleaningDialog').dialog('close');
                        }
                    }
                })
            }
        },
    })
});

function getPostDataFromTable(tableId, firstField, secondField){
    var tableRows = $('#'+tableId).datagrid('getData').rows;
    var dataObj = new Object();
    for(var i in tableRows){
        dataObj[tableRows[i][firstField]] = tableRows[i][secondField];
    }
    return JSON.stringify(dataObj);
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
    $(this).combobox('checkSelect',$(this));
    switch (record.value){
        case 1:
            $('#days').next().show().end().combobox('enable').combobox('enableValidation');
            $('.week_day').hide();
            break;
        case 2:
            $('#days').combobox('disableValidation').combobox('disable').next().hide();
            $('.week_day').show();
            break;
        case 3:
            $('.week_day').hide();
            $('#days').combobox('disableValidation').combobox('disable').next().hide();

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
        columns:[[
            {field:'checkbox',checkbox:true},
            {field:'name',title:'任务名称',width:'15%'},
            {field:'flag',hidden:true, width:'10%'},
            {field:'flagShow',title:'启用状态',width:'10%', formatter:function (v, r, i) {
                if(r.flag){
                    return '启用'
                }else{
                    return '禁用'
                }
            }},
            {field:'status',hidden:true,width:'10%'},
            {field:'statusShow',title:'执行状态',width:'10%', formatter: function (v, r, i) {
                if(r.status == 1){
                    return '正在执行'
                }else if(r.status == 2){
                    return '执行出错'
                }else{
                    return '空闲'
                }
            }},
            {field:'timeType',title:'执行时间类型',width:'18%'},
            {field:'timeStr',title:'执行时间串',width:'20%'},
            {field:'description',title:'任务描述',width:'20%'},
            {field:'oper',title:'操作',width:'15%',formatter:operationCleaningRules},
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
}


function searchRules(search, list){
    $(search).searchbox({
        prompt:'请输入搜索条件',
        height:24,
        width:200,
        searcher:function(v,n){
           $(list).datagrid('load', {condition:v})
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
                '<a class="easyui-linkbutton startCleaning" onclick="startCleaning('+row.id+')" data-options="iconCls:\'icon-redo\'" title="立即执行" style="margin-right: 5px;"></a>' +
                '<a class="easyui-linkbutton editCleaning" onclick="editCleaning('+index+')" data-options="iconCls:\'icon-edit\'" title="编辑" style="margin-right: 5px;"></a>' +
                '<a class="easyui-linkbutton delCleaning" onclick="delCleaning('+index+')" data-options="iconCls:\'icon-cancel\'" title="删除" ></a>'
    }
}


function addCleaning(){
    initDialog('#cleaningDialog','#table3','增加清洗任务');
    //initData(false,[]);
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
}

function editCleaning(i){
    var data = getEditData(i, '#table3');
    if(data == false)
        return false;
    initDialog('#cleaningDialog','#table3','修改清洗任务',data);
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

    var length = $('#next_save').linkbutton('options').lengths;
    for(var i = 0; i < length ; i++){
        $('#next_save').click();
        if(i == 0){
            $('input[name="timeType"]').each(function(){
                if($(this).val() == data.timeType){
                    $(this).attr('checked',true);
                    $(this).change()
                }
            })

            var time = $.parseJSON(data.timeStr);
            switch (data.timeType){
                case 1:
                    if(time.week != '*') {
                        $('#cycle').combobox('select', 2);

                        $('input[name="week_day"]').each(function(){
                            if($.inArray($(this).val(), time.week) != -1)
                                $(this).attr('checked',true);
                        })
                        $('#hours').combobox('select',time.hour);
                        $('#minutes').combobox('select',time.min);
                    }else if(time.day != '*'){
                        $('#cycle').combobox('select', 1);
                        $('#days').combobox('select',time.day);
                        $('#hours').combobox('select',time.hour);
                        $('#minutes').combobox('select',time.min);

                    }else{
                        $('#cycle').combobox('select', 3);
                        $('#hours').combobox('select',time.hour);
                        $('#minutes').combobox('select',time.min);
                    }
                    break;
                case 2:
                    var value = time.month + '/'+ time.day + '/'+time.year+' '+ time.hour +':'+time.min;
                    $('#once_time').datetimebox('setValue', value);
                    break;
                case 3:
                    break;
                case 4:
                    $('#intervalDay').combobox('select', time.day);
                    $('#hours').combobox('select',time.hour);
                    $('#minutes').combobox('select',time.min);
                    break;
                default:
                    $.messager.alert('错误', '调度计划类型错误',error);
                    return false;
            }

        }
        if(i==length-1){
            $('#fieldMapList').datagrid('loadData', getLoadDataFromData(data.fromFieldAndToField, 'fromFieldName', 'toFieldName'));
            $('#fieldCheckList').datagrid('loadData', getLoadDataFromData(data.fromFieldAndCheckRule, 'fromFieldName', 'ruleID'));
            $('#fieldCleanList').datagrid('loadData', getLoadDataFromData(data.fromFieldAndCleanRule, 'fromFieldName', 'ruleID'));
        }
    }

}

function delCleaning(i){
    var ids = getDelIDList(i, '#table3');
    if(ids){
        $.messager.confirm('确认', "确认要删除该任务？操作不可还原！", function (r) {
            if(r){
                saveDel(urls['deleteUrl'], '#table3', ids);
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
            $('#table3').datagrid('reload');
        }
    }, 'json');
}

function startCleaning(id){
    $.post(urls['startUrl'], {id: id}, function (msg) {
        if (msg.errorCode != '0x0000') {
            $.messager.alert('错误', msg.errorString, 'error');
        }else {
            $.messager.alert('成功', msg.errorString, 'success');
            $('#table3').datagrid('reload');
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


function addFieldCheck(){
    initDialog('#fieldCheckDialog','#fieldCheckList','增加校验规则');
    $('input[name="fieldCheckAction"]').val('add');
}

function editFieldCheck(i){
    var data = getEditData(i, '#fieldCheckList');
    if(data == false)
        return false;
    initDialog('#fieldCheckDialog','#fieldCheckList','修改校验规则', data)
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
    $('input[name="fieldCleanAction"]').val('add');
}

function editFieldClean(i){
    var data = getEditData(i, '#fieldCleanList');
    if(data == false)
        return false;
    initDialog('#fieldCleanDialog','#fieldCleanList','修改字典转换', data);
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

function addFieldMap(){
    initDialog('#fieldMapDialog','#fieldMapList','增加字段映射');
    $('input[name="fieldMapAction"]').val('add');
}

function editFieldMap(i){
    var data = getEditData(i, '#fieldMapList');
    if(data == false)
        return false;
    initDialog('#fieldMapDialog','#fieldMapList','修改字段映射', data);
    $('input[name="fieldMapAction"]').val('edit');
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

function addFieldMapToGrid(){
    var isValid = $('#fieldMapForm').form('validate');
    if(!isValid)
        return false;
    var data = $('#fieldMapForm').serializeArray();
    var rows = $('#fieldMapList').datagrid('getData');
    var temp = {}
    for(var i in data){
        temp[data[i].name] = data[i].value
    }
    for(var i in rows.rows){
        if(temp.toFieldName == rows.rows[i].toFieldName) {
            $.messager.alert('错误','该标准字段已经被映射','error');
            return false;
        }
    }
    if($('input[name="fieldMapAction"]').val() == 'add') {
        temp.oper = operationFieldMap('', temp, rows.total)
        $('#fieldMapList').datagrid('appendRow', temp);
        $('.edit').linkbutton({iconCls: 'icon-edit'})
        $('.del').linkbutton({iconCls: 'icon-cancel'})
    }else{
        console.log($('#fieldMapList').datagrid('getRowIndex', $('#fieldMapList').datagrid('getSelected')));
        $('#fieldMapList').datagrid('updateRow',{
            index:$('#fieldMapList').datagrid('getRowIndex', $('#fieldMapList').datagrid('getSelected')),
            row:temp,
        })
    }
    $('#fieldMapDialog').dialog('close');
    $('#fieldMapList').datagrid('clearSelections');
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
    for(var i in rows.rows){
        if(temp.fromFieldName == rows.rows[i].fromFieldName) {
            $.messager.alert('错误','该采集字段已经被映射','error')
            return false;
        }
    }
    if($('input[name="fieldCheckAction"]').val() == 'add') {
        temp.oper = operationFieldCheck('', temp, rows.total);
        $('#fieldCheckList').datagrid('appendRow', temp);
        $('.edit').linkbutton({iconCls: 'icon-edit'});
        $('.del').linkbutton({iconCls: 'icon-cancel'});
    }else{
        console.log($('#fieldCheckList').datagrid('getRowIndex', $('#fieldCheckList').datagrid('getSelected')));
        $('#fieldCheckList').datagrid('updateRow',{
            index:$('#fieldCheckList').datagrid('getRowIndex', $('#fieldCheckList').datagrid('getSelected')),
            row:temp,
        })
    }
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
    for(var i in rows.rows){
        if(temp.fromFieldName == rows.rows[i].fromFieldName) {
            $.messager.alert('错误','该采集字段已经被映射','error')
            return false;
        }
    }
    if($('input[name="fieldCleanAction"]').val() == 'add') {
        temp.oper = operationFieldClean('', temp, rows.total);
        $('#fieldCleanList').datagrid('appendRow', temp);
        $('.edit').linkbutton({iconCls: 'icon-edit'});
        $('.del').linkbutton({iconCls: 'icon-cancel'});
    }else{
        console.log($('#fieldCleanList').datagrid('getRowIndex', $('#fieldCleanList').datagrid('getSelected')));
        $('#fieldCleanList').datagrid('updateRow',{
            index:$('#fieldCleanList').datagrid('getRowIndex', $('#fieldCleanList').datagrid('getSelected')),
            row:temp,
        })
    }
    $('#fieldCleanDialog').dialog('close');
    $('#fieldCleanList').datagrid('clearSelections');
}