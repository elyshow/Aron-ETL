$(function(){
    $('#checkRuleType').tabs({
        onSelect:function(title,index){
            switch(index){
                case 0:
                    loadDataList({
                        list: '#checkFormatList',
                        url: urls['getCheckRuleListUrl'],
                        type: index,
                        toolbar: '#checkRuleToolBar',
                    });
                    //$(this).tabs('options').clicks[index]++;
                    searchRules('#checkFormatList','#checkRuleSearch','#checkRuleType');
                    break;
                case 1:
                    loadDataList({
                        list: '#checkNullList',
                        url: urls['getCheckRuleListUrl'],
                        type: index,
                        toolbar: '#checkRuleToolBar',
                    });
                   // $(this).tabs('options').clicks[index]++;
                    searchRules('#checkNullList','#checkRuleSearch','#checkRuleType');
                    break;
                case 2:
                    loadDataList({
                        list: '#checkLengthList',
                        url: urls['getCheckRuleListUrl'],
                        type: index,
                        toolbar: '#checkRuleToolBar',
                    });
                    searchRules('#checkLengthList','#checkRuleSearch','#checkRuleType');
                   // $(this).tabs('options').clicks[index]++;
                    break;
                case 3:
                    loadDataList({
                        list: '#checkCodeList',
                        url: urls['getCheckRuleListUrl'],
                        type: index,
                        toolbar: '#checkRuleToolBar',
                    });
                    searchRules('#checkCodeList','#checkRuleSearch','#checkRuleType');
                    //$(this).tabs('options').clicks[index]++;
                    break;
                default:
                    $.messager.alert('错误', 'tab选项卡无选中', 'error')
                    break;
            }
        }
    })

    $('#cleanRuleType').tabs({
        onSelect:function(title, index){
            switch (index){
                case 0:
                    loadCleanRulesList({
                        list:'#cleanRuleDictList',
                        url:urls['getCleanRuleListUrl'],
                        type:index,
                        toolbar:'#cleanRuleToolBar',
                        checkBtn:'checkCleanButton',
                        operation:'operationCleaningDictRules',
                        search:'#cleanRuleSearch',
                    });
                    break;
                case 1:
                    console.log(2);
                    loadCleanRulesList({
                        list:'#cleanRuleCodeList',
                        url:urls['getCleanRuleListUrl'],
                        type:index,
                        toolbar:'#cleanRuleCodeToolBar',
                        checkBtn:'checkCleanCodeButton',
                        operation:'operationCleaningRulesCode',
                        search:'#cleanRuleCodeSearch',
                    });
                    break;
                default:
                    $.messager.alert('错误', 'tab选项卡无选中', 'error')
                    break;
            }
        }
    });

     $('#ruleType').tabs({
        onSelect:function(title, index){
            switch (index){
                case 0 :
                    $('#checkRuleType').tabs('unselect', 0).tabs('select', 0);
                    break;
                case 1:
                    $('#cleanRuleType').tabs('unselect', 0).tabs('select', 0);
                    break;
                default:
                    $.messager.alert('错误', 'tab选项卡无选中', 'error')
                    break;
            }
        }
    }).tabs('unselect', 0).tabs('select', 0);
});

function addCleanRuleCode(){
     initDialog('#cleanRulesCodeDialog','#cleanRuleCodeList','增加代码转换');
    //$('input[name="dictTransAction"]').val('add');
	$('#cleanRulesCodeDialog input[name="id"]').val('');
}

function editCleanRuleCode(i){
    var data = getEditData(i, '#cleanRuleCodeList');
	id = getListID('#cleanRuleType');
    //var data = getEditData(i, id)
    if(data == false)
        return false;
    initDialog('#cleanRulesCodeDialog','#cleanRuleCodeList','修改代码转换', data);
   // $('input[name="dictTransAction"]').val('edit');
    $('input[name="id"]').val(data.id);
}

function delCleanRuleCode(i){
    if(i != undefined){
        var data = $('#cleanRuleCodeList').datagrid('getRows')[i],list = [];
        list.push(data)
    }else{
        var list = $('#cleanRuleCodeList').datagrid('getSelections');
        if(list.length == 0){
            $.messager.alert('错误',"请至少选择一条数据删除",'error')
            return false
        }
    }
    $.messager.confirm('确认', "确认要删除该规则？<h3 style='color: #ff0000;display: inline-block'>该操作不可还原！</h3>", function (r) {
        if(r){
          ids = '';
            for(var i in list){
                ids += list[i].id + ','
            }
            ids = ids.substr(0, ids.length - 1);
            $.post(urls['deleteCleanUrl'], {data:ids}, function(msg){
                if(msg.errorCode != '0x0000'){
                    $.messager.alert('错误',msg.errorString,'error');
                }else{
                    $('#cleanRuleCodeList').datagrid('reload');
                }
            }, 'json')
        }
    })
}

function operationCleaningRulesCode(v, r, i){
    return '<a class="edit" onclick="editCleanRuleCode('+i+')" data-options="iconCls:\'icon-edit\'" style="margin-right: 5px;" data-hover="编辑" title="编辑"></a>' +
            '<a class="del" onclick="delCleanRuleCode('+i+')" data-options="iconCls:\'icon-cancel\'" data-hover="删除" title="删除"></a>'
}

function saveCleanRuleCode(){
    var tab = $('#cleanRuleType').tabs('getSelected'),
        index = $('#cleanRuleType').tabs('getTabIndex', tab);

    $('#cleanRulesCodeForm').form('submit',{
        url:urls['saveCleanUrl'],
        onSubmit:function(param){
            return $(this).form('validate');
        },
        success:function (res) {
            res = $.parseJSON(res);
            if(res.errorCode!='0x0000'){
                $.messager.alert('错误', res.errorString, 'error');
            }else{
                $('#cleanRuleCodeList').datagrid('reload');
                $('#cleanRulesCodeDialog').dialog('close');
            }
        }
    })
}

function checkCleanCodeButton(v, r, i){
     var list = $('#cleanRuleCodeList').datagrid('getSelections');
    if(list.length == 0){
        $('#editCleanRulesCodeBtn').linkbutton('disable');
        $('#delCleanRulesCodeBtn').linkbutton('disable');
    }else if(list.length > 1 ){
        $('#editCleanRulesCodeBtn').linkbutton('disable');
        $('#delCleanRulesCodeBtn').linkbutton('enable');
    }else{
        $('#editCleanRulesCodeBtn').linkbutton('enable');
        $('#delCleanRulesCodeBtn').linkbutton('enable');
    }
}

function loadCleanRulesList(obj){
    $(obj.list).datagrid({
                url:obj.url ,
                queryParams:{
                    type: obj.type,
                },
                method:'post',
                toolbar:obj.toolbar,
                onSelect:window[obj.checkBtn],
                onSelectAll:window[obj.checkBtn],
                onUnselect:window[obj.checkBtn],
                onUnselectAll:window[obj.checkBtn],
                columns:[[
                    {field:'checkbox',checkbox:true},
                    {field:'name',title:'校验规则名称',width:'20%'},
                    {field:'type',title:'规则类型',width:'20%',formatter:function (v, r, i) {
                         if(r.type == 0){
                             return '字典转换'
                         } else{
                             return '代码转换'
                         }
                    }},
                    {field:'content',title:'规则内容',width:'20%'},
                    {field:'description',title:'规则描述',width:'20%'},
                    {field:'oper',title:'操作',width:'18%',formatter:window[obj.operation]},
                ]],
                onLoadSuccess:function(){
                    $('.edit').linkbutton({'iconCls':'icon-edit'})
                    $('.del').linkbutton({'iconCls':'icon-cancel'})
                    window[obj.checkBtn]();
                },
            });
            searchRules(obj.list, obj.search);
}

function searchRules(list, search, tabs){
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
            }
        }
    })
}

function loadDataList(obj){
    $(obj.list).datagrid({
        url:obj.url ,
        queryParams:{
            type: obj.type,
        },
        method:'post',
        toolbar:obj.toolbar,
        onSelect:checkButton,
        onSelectAll:checkButton,
        onUnselect:checkButton,
        onUnselectAll:checkButton,
        columns:[[
            {field:'checkbox',checkbox:true},
            {field:'name',title:'校验规则名称',width:'20%'},
            {field:'type',title:'规则类型',width:'20%',formatter:function (v, r, i) {
							if(r.type == 0){
								return '格式校验'
								 // return '<img src="/static/images/logo.png" style="width: 100px;height: 100px"/>'
							}else if(r.type == 1){
								return '空值校验'
							}else if(r.type == 2){
								return '长度及范围校验'
							}else if(r.type == 3){
								return '代码校验'
							}
                        }},
            {field:'content',title:'规则内容',width:'20%'},
            {field:'description',title:'规则描述',width:'20%'},
            {field:'oper',title:'操作',width:'18%',formatter:operationCleaningRules},
        ]],
        onLoadSuccess:function(){
            $('.edit').linkbutton({'iconCls':'icon-edit'})
            $('.del').linkbutton({'iconCls':'icon-cancel'})
            //$.parser.parse();
            checkButton()
        },
    });
}

function checkButton(){
    var tab = $('#checkRuleType').tabs('getSelected'),
        id = tab.find('table:hidden').attr('id'),
        list = $('#' + id).datagrid('getSelections');
    if(list.length == 0){
        $('#editCheckRulesBtn').linkbutton('disable');
        $('#delCheckRulesBtn').linkbutton('disable');
    }else if(list.length > 1 ){
        $('#editCheckRulesBtn').linkbutton('disable');
        $('#delCheckRulesBtn').linkbutton('enable');
    }else{
        $('#editCheckRulesBtn').linkbutton('enable');
        $('#delCheckRulesBtn').linkbutton('enable');
    }
}

function operationCleaningRules(value,row,index) {
    return '<a data-hover="编辑" title="编辑" class="edit" onclick="editCheckRules('+index+')" data-options="iconCls:\'icon-edit\'" style="margin-right: 5px;"></a>' +
            '<a data-hover="删除" title="删除" class="del" onclick="delCheckRules('+index+')" data-options="iconCls:\'icon-cancel\'"></a>'
}

function editCheckRules(i){
    id = getListID('#checkRuleType');
    var data = getEditData(i, id)
    if(data == false){
        return false;
    }
    initDialog('#checkRulesDialog','#checkFormatList', '修改规则', data);
    $('input[name="save_type"]').val('edit');
    $('input[name="id"]').val(data.id);
    var index = String($('#checkRuleType').tabs('getTabIndex', $('#checkRuleType').tabs('getSelected')))
    $('#checkRuleTypeCombo').combobox('select', index);

    if(index === "0"){
        $('#checkRuleTypeCombo').combobox('setText', '格式校验')
    }
}

function getListID(tabID){
    var tab = $(tabID).tabs('getSelected'),
        index = $(tabID).tabs('getTabIndex',tab),listID;

    switch(index){
        case 0:
            listID = '#checkFormatList';
            break;
        case 1:
            listID = '#checkNullList';
            break;
        case 2:
            listID = '#checkLengthList';
            break;
        case 3:
            listID = '#checkCodeList';
            break;
    }

    return listID;

}


function getEditData(i, listID){
    if(i != undefined){
        var data = $(listID).datagrid('getRows')[i]
    }else{
        var list = $(listID).datagrid('getSelections');
        if(list.length == 0){
            $.messager.alert('错误',"请至少选择一条数据修改",'error')
            return false
        }else if(list.length > 1){
            $.messager.alert('错误',"一次只能修改一条数据",'error')
            return false
        }else{
            var data =  $(listID).datagrid('getSelected');
        }
    }
    return data;
}

function addCheckRule(){
    initDialog('#checkRulesDialog','#checkFormatList','增加校验规则');
    $('#checkRulesDialog input[name="save_type"]').val('add');
    $('#checkRulesDialog input[name="id"]').val('');
    var index = String($('#checkRuleType').tabs('getTabIndex', $('#checkRuleType').tabs('getSelected')))
    $('#checkRuleTypeCombo').combobox('select', index);

    if(index === "0"){
        $('#checkRuleTypeCombo').combobox('setText', '格式校验')
    }
}

function saveCheckRule(t){
    var tab = $('#checkRuleType').tabs('getSelected'),
        index = $('#checkRuleType').tabs('getTabIndex', tab),
        //panel = tab.find('div[class="panel"]'),
        //table = panel.eq(index).find('table'),
        id = tab.find('table:hidden').attr('id');

    console.log(id)
    $(t).linkbutton('saveChange', {
        form:'#checkRulesForm',
        datagrid:'#' + id,
        dialog:'#checkRulesDialog',
        url:urls['saveCheckUrl'],
    })
}

function delCheckRules(i){
	id = getListID('#checkRuleType');
    if(i != undefined){
        var data = $(id).datagrid('getRows')[i],list = [];
        list.push(data)
    }else{
        var list = $(id).datagrid('getSelections');
        if(list.length == 0){
            $.messager.alert('错误',"请至少选择一条数据删除",'error')
            return false
        }
    }
    $.messager.confirm('确认', "确认要删除该规则？<h3 style='color: #ff0000;display: inline-block'>该操作不可还原！</h3>", function (r) {
        if(r){
            ids = '';
            for(var i in list){
                ids += list[i].id + ','
            }
            ids = ids.substr(0, ids.length - 1);
            $.post(urls['deleteCheckUrl'], {data:ids}, function(msg){
                if(msg.errorCode != '0x0000'){
                    $.messager.alert('错误',msg.errorString,'error');
                }else{
                    $(id).datagrid('reload');
                }
            }, 'json')
        }
    })
}

function checkCleanButton() {
    var list = $('#cleanRuleDictList').datagrid('getSelections');
    if(list.length == 0){
        $('#editCleanRulesBtn').linkbutton('disable');
        $('#delCleanRulesBtn').linkbutton('disable');
    }else if(list.length > 1 ){
        $('#editCleanRulesBtn').linkbutton('disable');
        $('#delCleanRulesBtn').linkbutton('enable');
    }else{
        $('#editCleanRulesBtn').linkbutton('enable');
        $('#delCleanRulesBtn').linkbutton('enable');
    }
}

function operationCleaningDictRules(value,row,index) {
     return '<a data-hover="编辑" title="编辑" class="edit" onclick="editCleanRule('+index+')" data-options="iconCls:\'icon-edit\'" style="margin-right: 5px;"></a>' +
            '<a data-hover="删除" title="删除" class="del" onclick="delCleanRule('+index+')" data-options="iconCls:\'icon-cancel\'"></a>'
}

function addCleanRule(){

    initDialog('#cleanRulesDialog','#cleanRuleDictList','增加清洗规则');
    $('#cleanRulesDialog input[name="id"]').val('');

    var index = String($('#cleanRuleType').tabs('getTabIndex', $('#cleanRuleType').tabs('getSelected')))
    $('#cleanRuleTypeCombo').combobox('select', index);

    if(index === "0"){
        $('#cleanRuleTypeCombo').combobox('setText', '字典转换')
    }
    $('#dictTransList').datagrid({
        toolbar: '#dictTransToolBar',
        fit:true,
        columns: [[
            {field: 'checkbox', checkbox: true},
            {field: 'fromContent', title: '源内容', width: '20%'},
            {field: 'toContent', title: '转换后内容', width: '20%'},
            {field: 'oper', title: '操作', width: '14%', formatter: operationDictTrans}
        ]],
        onLoadSuccess: function (data) {
            $('.edit').linkbutton({iconCls: 'icon-edit'});
            $('.del').linkbutton({iconCls: 'icon-cancel'});
        }
    });
    searchRules('#dictTransList', '#dictTransSearch',  '#cleanRuleType');
    $('#dictTransList').datagrid('loadData', []);
}

function editCleanRule(i) {
    var data = getEditData(i, '#cleanRuleDictList')
    if(data == false){
        return false;
    }
    initDialog('#cleanRulesDialog','#cleanRuleDictList','修改清洗规则', data);
    $('input[name="id"]').val(data.id);
    $('#dictTransList').datagrid({
        toolbar: '#dictTransToolBar',
        fit:true,
        columns: [[
            {field: 'checkbox', checkbox: true},
            {field: 'fromContent', title: '源内容', width: '20%'},
            {field: 'toContent', title: '转换后内容', width: '20%'},
            {field: 'oper', title: '操作', width: '14%', formatter: operationDictTrans}
        ]],
        onLoadSuccess: function (data) {
            $('.edit').linkbutton({iconCls: 'icon-edit'});
            $('.del').linkbutton({iconCls: 'icon-cancel'});
        }
    });
    var index = String($('#cleanRuleType').tabs('getTabIndex', $('#cleanRuleType').tabs('getSelected')))
    $('#cleanRuleTypeCombo').combobox('select', index);

    if(index === "0"){
        $('#cleanRuleTypeCombo').combobox('setText', '字典转换')
    }
    searchRules('#dictTransList', '#dictTransSearch',  '#cleanRuleType');
    var dataObj = $.parseJSON(data.content.replace(/\\/g,'\\\\'));
    var dataObjList = [];
    for(var key in dataObj){
        var tmp = new Object();
        tmp['fromContent'] = key;
        tmp['toContent'] = dataObj[key];
        dataObjList.push(tmp);
    }
    $('#dictTransList').datagrid('loadData', dataObjList);
}

function saveCleanRule(t){
    var tab = $('#cleanRuleType').tabs('getSelected'),
        index = $('#cleanRuleType').tabs('getTabIndex', tab);

    $('#cleanRulesForm').form('submit',{
        url:urls['saveCleanUrl'],
        onSubmit:function(param){

            var tableRows = $('#dictTransList').datagrid('getData').rows;
            var dataObj = new Object();
            for(var i in tableRows){
                dataObj[tableRows[i]['fromContent']] = tableRows[i]['toContent'];
            }

            param.content = JSON.stringify(dataObj).replace(/\\\\/g,'\\');
            return $(this).form('validate');
        },
        success:function (res) {
            res = $.parseJSON(res);
            if(res.errorCode!='0x0000'){
                $.messager.alert('错误', res.errorString, 'error');
            }else{
                $('#cleanRuleDictList').datagrid('reload');
                $('#cleanRulesDialog').dialog('close');
            }
        }
    })
}

function delCleanRule(i) {
    if(i != undefined){
        var data = $('#cleanRuleDictList').datagrid('getRows')[i],list = [];
        list.push(data)
    }else{
        var list = $('#cleanRuleDictList').datagrid('getSelections');
        if(list.length == 0){
            $.messager.alert('错误',"请至少选择一条数据删除",'error')
            return false
        }
    }
    $.messager.confirm('确认', "确认要删除该规则？<h3 style='color: #ff0000;display: inline-block'>该操作不可还原！</h3>", function (r) {
        if(r){
            ids = '';
            for(var i in list){
                ids += list[i].id + ','
                console.log(ids);
            }
            ids = ids.substr(0, ids.length - 1);
            $.post(urls['deleteCleanUrl'], {data:ids}, function(msg){
                if(msg.errorCode != '0x0000'){
                    $.messager.alert('错误',msg.errorString,'error');
                }else{
                    $('#cleanRuleDictList').datagrid('reload');
                }
            }, 'json')
        }
    })
}

function operationDictTrans(v, r, i){
    return '<a data-hover="编辑" title="编辑" onclick="editDictTrans('+i+')" class="edit" style="margin-right: 5px;"></a>' +
            '<a data-hover="删除" title="删除" onclick="delDictTrans('+i+')" class="del" title="" ></a>'
}


function addDictTrans(){
    initDialog('#dictTransDialog','#dictTransList','增加字典转换');
    $('input[name="dictTransAction"]').val('add');
}

function editDictTrans(i) {
    var data = getEditData(i, '#dictTransList');
    if(data == false)
        return false;
    initDialog('#dictTransDialog','#dictTransList','修改字典转换', data);
    $('input[name="dictTransAction"]').val('edit');
}

function delDictTrans(i) {
    var ids = [];
    if(i != undefined){
        ids.push(i)
    }else{
        var list = $('#dictTransList').datagrid('getSelections');
        if(list.length == 0){
            $.messager.alert('错误',"请至少选择一条数据删除",'error');
            return false
        }
        for(var j in list){
            ids.unshift($('#dictTransList').datagrid('getRowIndex',list[j]))
        }
    }
    $.messager.confirm('确定提示框','是否确定删除选中记录？',function(ok){
        if(ok){
            for(var i in ids){
                $('#dictTransList').datagrid('deleteRow',ids[i])
            }
        }
    })
}

function addDictTransToGrid(){
    var isValid = $('#dictTransForm').form('validate');
    if(!isValid)
        return false;
    var data = $('#dictTransForm').serializeArray();
    var rows = $('#dictTransList').datagrid('getData');
    var temp = {}
    for(var i in data){
        temp[data[i].name] = data[i].value
    }
    if($('#dictTransDialog input[name="dictTransAction"]').val() == 'add') {
         for(var i in rows.rows){
            if(temp.fromContent == rows.rows[i].fromContent) {
                $.messager.alert('错误','键值已存在','error');
                return false;
            }
        }
        temp.oper = operationDictTrans('', temp, rows.total)
        $('#dictTransList').datagrid('appendRow', temp);

    }else{
        $('#dictTransList').datagrid('updateRow',{
            index:$('#dictTransList').datagrid('getRowIndex', $('#dictTransList').datagrid('getSelected')),
            row:temp,
        }).datagrid('clearSelections');
    }
    $('.edit').linkbutton({iconCls: 'icon-edit'});
    $('.del').linkbutton({iconCls: 'icon-cancel'});
    $('#dictTransDialog').dialog('close');
    $('#dictTransList').datagrid('clearSelections');
}