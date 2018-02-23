$(function(){
    $('#permissionList').datagrid({
        onSelect:checkBtn,
        onUnselect:checkBtn,
        onSelectAll:checkBtn,
        onUnselectAll:checkBtn,
        columns:[[
            {field:'checkbox',checkbox:true},
            {field:'name',title:'权限名称',width:'35%'},
            {field:'url',title:'权限地址',width:'35%'},
            {field:'opera',title:'操作',width:'25%',formatter:operationPermissionList}
        ]],
        onLoadSuccess:function(){
            $('.edit').linkbutton({iconCls: 'icon-edit',});
            $('.del').linkbutton({iconCls: 'icon-cancel'});
            checkBtn()
        },
    });
    search('#permissionList', '#permissionListSearch')
})

function operationPermissionList(value, row, index){
    return '<a class="edit" onClick="editPermissionList('+index+')" style="margin-right: 5px" title="编辑"></a>'
         + '<a class="del" onClick="delPermissionList('+index+')" title="删除"></a>'
}


function checkBtn(){
    var rows = $('#permissionList').datagrid('getSelections')
    if(rows.length == 0){
        $('#editPermissionListBtn,#delPermissionListBtn').linkbutton('disable')
    }else if(rows.length == 1){
        $('#editPermissionListBtn,#delPermissionListBtn').linkbutton('enable')
    }else{
        $('#editPermissionListBtn').linkbutton('disable')
        $('#delPermissionListBtn').linkbutton('enable')
    }
}

function addPermissionList(){
    initDialog('#permissionListDialog', '#permissionList', '新增权限')
    $('#id').val('')
}

function editPermissionList(i){
    var data = getEditData(i, '#permissionList')
    if(data == false)
        return
    initDialog('#permissionListDialog', '#permissionList', '编辑权限', data)
}

function delPermissionList(i){
    var data = getDelIDList(i, '#permissionList')
    if(data == false)
        return
    $.messager.confirm('提示','是否删除选中记录', function(ok){
        if(ok){
            $.post(urls['deletepermissionurl'], {ids:data}, function(msg){
                if(msg.errorCode != '0x0000'){
                    $.messager.alert('错误', msg.errorString, 'error')
                }else{
                    $('#permissionList').datagrid('reload')
                }
            }, 'json')
        }
    })
}

function savePermissionList(){
    var id = $('input[name="id"]').val()
    console.log(id)
    if(id == '' || id == undefined){
        var url = urls['addpermissionurl']
    }else{
        var url = urls['editpermissionurl']
    }
    $('#permissionListForm').form('submit', {
        url:url,
        onSubmit:function(param){
            return $(this).form('validate')
        },
        success:function(msg){
            msg = $.parseJSON(msg)
            if(msg.errorCode != '0x0000'){
                $.messager.alert('错误', msg.errorString, 'error')
            }else{
                $('#permissionListDialog').dialog('close')
                $('#permissionList').datagrid('reload')
            }
        }
    })
}