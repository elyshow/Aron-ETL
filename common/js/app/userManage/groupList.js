$(function(){
    $('#groupList').datagrid({
        onSelect:checkBtn,
        onUnselect:checkBtn,
        onSelectAll:checkBtn,
        onUnselectAll:checkBtn,
        columns:[[
            {field:'checkbox',checkbox:true},
            {field:'name',title:'用户组名',width:'50%'},
            {field:'opera',title:'操作',width:'45%',formatter:operationGroupList}
        ]],
        onLoadSuccess:function(){
            $('.edit').linkbutton({iconCls: 'icon-edit',});
            $('.del').linkbutton({iconCls: 'icon-cancel'});
            checkBtn()
        },
    });
    search('#groupList', '#groupListSearch')
    $('#cc').combobox({
        url:urls['getnameurl'],
        method:'post',
        valueField:'id',
        textField:'name',
        panelHeight:'auto',
        multiple:true,
        formatter: function (row) {
            var opts = $(this).combobox('options');
            return '<input type="checkbox" class="combobox-checkbox">' + row[opts.textField]
        },
        onLoadSuccess: function () {
            var opts = $(this).combobox('options');
            var target = this;
            var values = $(target).combobox('getValues');
            $.map(values, function (value) {
                var el = opts.finder.getEl(target, value);
                el.find('input.combobox-checkbox')._propAttr('checked', true);
            })
        },
        onSelect: function (row) {
            $(this).combobox('checkSelect')
            var opts = $(this).combobox('options');
            var el = opts.finder.getEl(this, row[opts.valueField]);
            el.find('input.combobox-checkbox')._propAttr('checked', true);
        },
        onUnselect: function (row) {
            var opts = $(this).combobox('options');
            var el = opts.finder.getEl(this, row[opts.valueField]);
            el.find('input.combobox-checkbox')._propAttr('checked', false);
        }
    });
})

function operationGroupList(value, row, index){
    return '<a class="edit" onClick="editGroupList('+index+')" style="margin-right: 5px" title="编辑"></a>'
         + '<a class="del" onClick="delGroupList('+index+')" title="删除"></a>'
}


function checkBtn(){
    var rows = $('#groupList').datagrid('getSelections')
    if(rows.length == 0){
        $('#editGroupListBtn,#delGroupListBtn').linkbutton('disable')
    }else if(rows.length == 1){
        $('#editGroupListBtn,#delGroupListBtn').linkbutton('enable')
    }else{
        $('#editGroupListBtn').linkbutton('disable')
        $('#delGroupListBtn').linkbutton('enable')
    }
}

function addGroupList(){
    initDialog('#groupListDialog', '#groupList', '新增用户组')
    $('#id').val('')
    
}

function editGroupList(i){
    var data = getEditData(i, '#groupList')
    if(data == false)
        return
    initDialog('#groupListDialog', '#groupList', '编辑用户组', data)
}

function delGroupList(i){
    var data = getDelIDList(i, '#groupList')
    if(data == false)
        return
    $.messager.confirm('提示','是否删除选中记录', function(ok){
        if(ok){
            $.post(urls['deletegroupurl'], {ids:data}, function(msg){
                if(msg.errorCode != '0x0000'){
                    $.messager.alert('错误', msg.errorString, 'error')
                }else{
                    $('#groupList').datagrid('reload')
                }
            }, 'json')
        }
    })
}

function saveGroupList(){
    var id = $('input[name="id"]').val()
    console.log(id)
    if(id == '' || id == undefined){
        var url = urls['addgroupurl']
    }else{
        var url = urls['editgroupurl']
    }
    $('#groupListForm').form('submit', {
        url:url,
        onSubmit:function(param){
            return $(this).form('validate')
        },
        success:function(msg){
            msg = $.parseJSON(msg)
            if(msg.errorCode != '0x0000'){
                $.messager.alert('错误', msg.errorString, 'error')
            }else{
                $('#groupListDialog').dialog('close')
                $('#groupList').datagrid('reload')
            }
        }
    })
}