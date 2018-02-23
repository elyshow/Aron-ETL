// // /*生成树*/
// $(function(){
//     $('#checkFormatList').treegrid({
//         url:'/catalogueManagement/getData/',
//         idField:'id',
//         treeField:'cataloguename',
//         columns:[[
//             {title:'目录结构',field:'cataloguename',width:180},
//             {field:'typetime',title:'创建时间',width:80},
//             {field:'oper',title:'操作',width:80},
//         ]],
//     });
// })
//
//
//
//
$(function(){
    $('#checkFormatList').treegrid({
        //url:'/catalogueManagement/getData/',
        idField:'id',
        treeField:'text',
        method:'post',
        toolbar:'#cleanRulesToolBar',
        onSelect:checkButton,
        onSelectAll:checkButton,
        onUnselect:checkButton,
        onUnselectAll:checkButton,
        columns:[[
            {title:'目录结构',field:'text',width:'30%'},
            {field:'typetime',title:'创建时间',width:'30%'},
            {field:'oper',title:'操作',width:'40%',formatter:operationCleaningRules},
        ]],
        onLoadSuccess:function(){
            // $.parser.parse();
            $('.add').linkbutton({iconCls:'icon-add'})
            $('.edit').linkbutton({iconCls:'icon-edit'})
            $('.del').linkbutton({iconCls:'icon-cancel'})
            checkButton()
        },
    });
})

function checkButton(){
    var list = $('#checkFormatList').treegrid('getSelections');
    if(list.length == 0){
        $('#editCleaningRulesBtn').linkbutton('disable')
        $('#delCleaningRulesBtn').linkbutton('disable')
    }else if(list.length > 1 ){
        $('#editCleaningRulesBtn').linkbutton('disable')
        $('#delCleaningRulesBtn').linkbutton('enable')
    }else{
        $('#editCleaningRulesBtn').linkbutton('enable')
        $('#delCleaningRulesBtn').linkbutton('enable')
    }
}

function operationCleaningRules(value,row,index) {
    console.log(value)
    console.log(row)
    console.log(index)
    return '<a class="add" onclick="addCleaningRules('+index+')" data-options="iconCls:\'icon-add\'" style="margin-right: 30px; margin-left: 60px;">添加</a>' +
           '<a class="edit" onclick="editCleaningRules('+index+')" data-options="iconCls:\'icon-edit\'" style="margin-right: 30px; ">编辑</a>' +
           '<a class="del" onclick="delCleaningRules('+index+')" data-options="iconCls:\'icon-cancel\'" style="margin-right: 30px;">删除</a>'
}

function editCleaningRules(i){
    console.log(i)
    if(i != undefined){
        var data = $('#checkFormatList').treegrid('getRows')[i]
     }else{
         var list = $('#checkFormatList').treegrid('getSelections');
        //  if(list.length == 0){
        //      $.messager.alert('错误',"请至少选择一条数据修改",'error')
        //     return false
        //  }else if(list.length > 1){
        //      $.messager.alert('错误',"一次只能修改一条数据",'error')
        //      return false
        // }else{
             if(list.length == 1){
                 var data =  $("#checkFormatList").treegrid('getSelected');
              //return false;
            // var data =  $("#checkFormatList").treegrid('getSelected');
        }
    }
    $('input[name="save_type"]').val('edit')
    $('input[name="id"]').val(data.id)
    $('#cataname').val(data.text).validatebox('validate');
    $('#combo_').val(data.typeparentid);
    initDialog('#cleaningRulesDialog','#checkFormatList' , '修改目录', data);
}

function addCleaningRules(i){
    if(i != undefined){
        var data = $('#checkFormatList').treegrid('getRows')[i]
    }else{
        var list = $('#checkFormatList').treegrid('getSelections');
        if(list.length == 0){
            $.messager.alert('错误',"请至少选择一条数据增加",'error')
            return false
        }else if(list.length > 1){
            $.messager.alert('错误',"一次只能增加一条数据",'error')
            return false
        }else{
            var data =  $("#checkFormatList").treegrid('getSelected');
        }
    }
    $('input[name="save_type"]').val('add')
    $('input[name="id"]').val(data.id)
    $('#cataname').val('');
    $('#combo_').val(data.typeparentid);
    initDialog('#cleaningRulesDialog','#checkFormatList' , '添加目录', data);
}



// function addCleaningRules(){
//     $('input[name="save_type"]').val('add')
//     $('input[name="id"]').val('')
//    initDialog('#cleaningRulesDialog','#checkFormatList','添加目录')
// }

function saveCleaningRules(t){
    $('#cleaningRulesForm').form('submit',{
        url:'/catalogueManagement/saveCleaningRules/',
        onSubmit:function(param){
            param.hierarchy = 1
        },
        success:function(msg){
            msg = $.parseJSON(msg)
            if(msg.errorCode != '0x0000'){
                $.messager.alert('错误', msg.errorString, 'error')
                return
            }else{
                $('#checkFormatList').treegrid('reload')
                $('#cleaningRulesDialog').dialog('close')
            }
        }
    })
}

function delCleaningRules(i){
    if(i != undefined){
        var data = $('#checkFormatList').treegrid('getRows')[i],list = [];
        list.push(data)
    }else{
       var list = $('#checkFormatList').treegrid('getSelections');
        if(list.length == 0){
            $.messager.alert('错误',"请至少选择一条数据删除",'error')
            return false
        }
    }
    ids = '';
    for(var i in list){
        ids += list[i].id + ','
    }
    ids = ids.substr(0, ids.length - 1);
    $.post('/catalogueManagement/delCleaningRules/', {data:ids}, function(msg){
        if(msg.errorCode != '0x0000'){
            $.messager.alert('错误',msg.errorString,'error');
        }else{
            $('#checkFormatList').treegrid('reload');
        }
    }, 'json')
}



