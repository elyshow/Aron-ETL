$(function(){
    $('#userList').datagrid({
        onSelect:checkBtn,
        onUnselect:checkBtn,
        onSelectAll:checkBtn,
        onUnselectAll:checkBtn,
        columns:[[
            {field:'checkbox',checkbox:true},
            {field:'username',title:'用户名',width:'20%'},
            {field:'group_name',title:'用户组',width:'20%'},
            {field:'department',title:'部门',width:'18%'},
            {field:'email',title:'Email',width:'10%'},
            {field:'telephone',title:'电话',width:'10%'},
            {field:'isActive',title:'状态',width:'10%',formatter:function(value,row,index){
                if(row.is_active == true){
                    return '已启用'
                }else
                    return '已禁用'
            }},
            {field:'opera',title:'操作',width:'10%',formatter:operationUserList}
        ]],
        onLoadSuccess:function(){
            $('.edit').linkbutton({iconCls: 'icon-edit',});
            $('.del').linkbutton({iconCls: 'icon-cancel'});
            $('.changePasswd').linkbutton({iconCls: 'icon-mini-refresh'});
            checkBtn()
        },
    });
    search('#userList', '#userListSearch')
})

function operationUserList(value, row, index){
    return '<a class="edit" onClick="editUserList('+index+')" style="margin-right: 5px" title="编辑"></a>'
         + '<a class="del" onClick="delUserList('+index+')" title="删除"></a>'
        + '<a class="changePasswd" onClick="openChangePasswdDialog('+row.id+')" title="修改密码"></a>'
}


function checkBtn(){
    var rows = $('#userList').datagrid('getSelections')
    if(rows.length == 0){
        $('#editUserListBtn,#delUserListBtn').linkbutton('disable')
    }else if(rows.length == 1){
        $('#editUserListBtn,#delUserListBtn').linkbutton('enable')
    }else{
        $('#editUserListBtn').linkbutton('disable')
        $('#delUserListBtn').linkbutton('enable')
    }
}

function addUserList(){
    initDialog('#userListDialog', '#userList', '新增用户');
    $('#tr_password').show();
    $('#id_password').validatebox('enable').validatebox('enableValidation');
    $('input[name="is_active"]').attr('checked',false);
    $('#id').val('');
}

function editUserList(i){
    var data = getEditData(i, '#userList')
    if(data == false)
        return
    initDialog('#userListDialog', '#userList', '编辑用户', data);
    $('#tr_password').hide();
    $('#id_password').validatebox('disableValidation').validatebox('disable');
    if(data.is_active == true)
        $('input[name="is_active"]').attr('checked','checked')
    else
        $('input[name="is_active"]').attr('checked',false)
}

function delUserList(i){
    var data = getDelIDList(i, '#userList')
    if(data == false)
        return
    $.messager.confirm('提示','是否删除选中记录', function(ok){
        if(ok){
            $.post(urls['deleteuserurl'], {ids:data}, function(msg){
                if(msg.errorCode != '0x0000'){
                    $.messager.alert('错误', msg.errorString, 'error')
                }else{
                    $('#userList').datagrid('reload')
                }
            }, 'json')
        }
    })
}

function saveUserList(){
    var id = $('input[name="id"]').val()
    console.log(id)
    if(id == '' || id == undefined){
        var url = urls['adduserurl']
    }else{
        var url = urls['edituserurl']
    }
    $('#userListForm').form('submit', {
        url:url,
        onSubmit:function(param){
            console.log($('input[name="is_active"]:checked').length)
            param.is_active = $('input[name="is_active"]:checked').length == 1 ? 'True' : 'False'
            return $(this).form('validate')
        },
        success:function(msg){
            msg = $.parseJSON(msg)
            if(msg.errorCode != '0x0000'){
                $.messager.alert('错误', msg.errorString, 'error')
            }else{
                $('#userListDialog').dialog('close')
                $('#userList').datagrid('reload')
            }
        }
    })
}

function openChangePasswdDialog(id) {
    $('#dialog_changePasswd').dialog({
        onOpen:function(){
            $('#changePasswdForm').form('clear');
            $('#changePasswdForm .textbox[name="id"]').val(id);
        },
    }).dialog('open')
}

function changePasswd() {
    $('#changePasswdForm').form('submit', {
        url:urls['resetpasswordurl'],
        onSubmit: function (param) {
            return $(this).form('validate');
        },
        success: function (msg) {
            msg = $.parseJSON(msg);
            if(msg.errorCode != '0x0000'){
                $.messager.alert('错误', msg.errorString, 'error')
            }else{
                $('#dialog_changePasswd').dialog('close');
                window.location.reload();
            }
        }
    });
}