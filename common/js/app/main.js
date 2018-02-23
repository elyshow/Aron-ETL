var input_width = 200, input_height = 24;

$(function(){
	$('.easyui-validatebox').css({
		width:(input_width-10),
		height:(input_height-2),
		padding:'0 4px',
	}).focus(function(){
		$(this).addClass('textbox-focused none_outline')
	}).blur(function(){
		$(this).removeClass('textbox-focused none_outline')
	})
});

/*
*为页面所有按钮绑定点击事件
* @param:type string 调用的方法名称
* @param:obj  object  调用方法需要传递的参数
* @return: void   无返回值
* */
function linkbutton_click(type,obj){
	$(this).linkbutton(type,obj);
}

function initDialog(dialog, list, title, data){
	if($(dialog).length == 0){
		$.messager.alert('错误','对话框不存在','error')
		return false;
	}
	if($(list).length == 0){
		$.messager.alert('错误','列表不存在','error')
		return false;
	}
	if(title == undefined){
		$.messager.alert('错误','标题不能为空','error')
		return false;
	}
    if(data == undefined){
        var fields = $(list).datagrid('getColumnFields');
        data = {}
        for (var i in fields)
            data[fields[i]] = ''
    }
    $(dialog).dialog({
        title:title,
        onOpen:function(){
            initData(true,dialog , data);
        },
        onClose:function(){
            initData(false, dialog,  data)
            $(list).datagrid('clearSelections')
        }
    }).dialog('open')
}


function initData(type, dialog, data){
    if($(dialog).length == 0){
		$.messager.alert('错误','对话框不存在','error')
		return false;
	}
    if(data == undefined)
        return false;
    for(var i in data){
        var value = type ? data[i] : '';
        if($(dialog).find('input[comboname="'+i+'"]').length != 0){
            try {
                $(dialog).find('input[comboname="'+i+'"]').combobox('select',value).combobox('validate');
            } catch (e) {

            }
        }else if($(dialog).find('input[textboxname="'+i+'"]').length != 0){
            $(dialog).find('input[textboxname="'+i+'"]').textbox('setValue',value).textbox('setText',value).textbox('validate');
        }else if($(dialog).find('input[name="'+ i +'"]').length != 0 && $(dialog).find('input[name="'+ i +'"]').hasClass('textbox')){
            $(dialog).find('input[name="'+ i +'"]').val(value).validatebox('validate');
        }else if($('input[name="'+i+'"][type="checkbox"]').length != 0 ){
            $(dialog).find('input[name="'+i+'"][type="checkbox"]').each(function(){
                if(type == false){
                    $(this).checked = false;
                }else{
                    if(value == $(this).val()) {
                        $(this).checked = true;
                    }
                }
            })
        }else if($(dialog).find('input[name="'+i+'"][type="radio"]').length != 0 ){
            if(type == false){
                $(dialog).find('input[name="'+i+'"][type="radio"]').eq(0).checked = true;
                //return;
            }else{
                $(dialog).find('input[name="'+i+'"][type="radio"]').each(function(){
                    if(value == $(this).val()) {
                        $(this).checked = true;
                        return
                    }
                })
            }

        }

    }
}

function search(list, search, otherCcondition){
    $(search).searchbox({
        prompt:'请输入搜索条件',
        height:24,
        width:200,
        searcher:function(v,n){
            var url = $(list).datagrid('options').url;
            if(url){
                var condition = {condition:v}
                if(otherCcondition != undefined)
                    $.extend(condition, otherCcondition);
                $(list).datagrid('load', condition)
            } else {
                $(list).datagrid('checkRow', v);
            }
        }
    })
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

function addFormToDataGrid(formId, listId, type, dialogId, preKey){
    var isValid = $(formId).form('validate');
    if(!isValid)
        return false;
    var data = $(formId).serializeArray();
    var rows = $(listId).datagrid('getData');
    var temp = {}
    for(var i in data){
        temp[data[i].name] = data[i].value
    }

    if(type == 'add') {
        for(var i in rows.rows){
            if(temp[preKey] == rows.rows[i][preKey]) {
                $.messager.alert('错误','该采集字段已经已处理','error')
                return false;
            }
        }
        temp.oper = operationFieldClean('', temp, rows.total);
        $(listId).datagrid('appendRow', temp);
    }else{
        $(listId).datagrid('updateRow',{
            index:$(listId).datagrid('getRowIndex', $(listId).datagrid('getSelected')),
            row:temp,
        });
    }
    $('.edit').linkbutton({iconCls: 'icon-edit'});
    $('.del').linkbutton({iconCls: 'icon-cancel'});
    $(dialogId).dialog('close');
    $(listId).datagrid('clearSelections');
}

