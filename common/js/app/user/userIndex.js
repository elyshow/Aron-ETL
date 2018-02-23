$(function(){
	$("#userList").datagrid({
		url:'/userIndex/userInfo/',
		toolbar:'#userToolBar',
		autoRowHeight:true,
		method:'post',
		columns:[[
			{field:'checkbox',checkbox:true},
			{field:'userid',title:'用户id',width:'15%',},
			{field:'username',title:'用户名称',width:'15%',},
			{field:'usertel',title:'联系方式',width:'20%',},
			{field:'usermail',title:'用户邮箱',width:'20%',},
			{field:'oper',title:'查看详情',width:'25%',formatter:func},
		]],
		onLoadSuccess:function(){
			$('.detailMore').linkbutton({
					iconCls: 'icon-more',
				});
			$('.detailEdit').linkbutton({
					iconCls: 'icon-edit',
				});
		}
	})

	$('#userTbas').tabs('disableTab', 1);
	$('#userTbas').tabs('disableTab', 2);


//搜索
	 $('#userSearchBox').searchbox({
        prompt:'请输入用户id搜索',
        height:24,
        width:200,
        searcher:function(v,n){
           $('#userList').datagrid('load', {condition:v,type:1});
			console.log(v);
			console.log('111');
        }
    })

 // 下一步tabs选项卡
		$('#user_basic_next').bind('click', function () {
		$('#userTbas').tabs('enableTab', 1);
		$('#userTbas').tabs('select', 1);
		usertype=$('input[name="userType"]:checked').val();
		$('#userTree').tree({
		url:'/userIndex/getTreeData/?data='+usertype,
		checkbox:true,
		lines:true,
		onLoadSuccess:function (node,data) {
			 // $('#userTree').tree("collapseAll");
			  var node = $('#userTree').tree('getRoot');
			  var children = $('#userTree').tree('getChildren',node.target);
			for(var i=0; i<children.length; i++){
				$('#userTree').tree('collapse', children[i].target)
			}
		}
	});
	})

// 下一步tabs选项卡
	$('#userper_sub').bind('click',function () {
		$('#userTbas').tabs('enableTab', 2);
		$('#userTbas').tabs('select', 2);
		$("#interList").datagrid({
		url:'/dataway/showData/',
		fit:false,
			width:586,
			height:390,
		columns:[[
			{field:'checkbox',checkbox:true},
			{field:'nameapi',title:'接口名称',align:'center',width:'30%',},
			{field:'idapi',title:'接口ID',align:'center',width:'25%',},
			{field:'createtime',title:'创建时间',align:'center',width:'40%',},
		]],
				onLoadSuccess:function (data) {
		}
	})

	})

	$("#comboBelong").combobox({
		url:'/userIndex/recognCombobox/',
		textField:'recognname',
		valueField:'recognid',
	})
})


function func(v,r,i){
	return  '<a class="detailMore" href="javascript:detailMore();"  data-options="" style="margin:8px 5px;">详情</a>'+
			'<a class="detailEdit" href="javascript:ModifyMore();"  data-options="" style="margin:8px 5px;">修改</a>'
}
//删除
function userDel() {
	var data = $("#userList").datagrid('getSelections');
	if(data.length == 0){
		$.messager.alert('警告','请至少选择一条数据','warning');
	}
	else {
		$.messager.confirm('确认删除框', '是否确定删除选中记录?', function (ok) {
			if (ok) {
				var ids = '';
				for (var i in data) {
					ids += data[i].userid + ',';
				}
				ids = ids.substr(0, ids.length - 1);
				$.get('/userIndex/userDel/', {data: ids}, function (msg) {
					$("#userList").datagrid('reload');
				})
			}
		})
	}
}

//查看详情
function detailMore() {
	var data = $("#userList").datagrid('getSelected');
	dataid=data.userid;
	datatype=data.usertype;
	console.log(datatype)
		linkbutton_click('open_dialog',{dialog:'#userDetailDialog'});
	        $(".userType").each(function () {
					if($(this).val()==datatype)
						$(this).attr('checked',true);
				});
			$('.username').val(data.username);
			$('.usertel').val(data.usertel);
			$('.usermail').val(data.usermail);
			$('.userother').val(data.userother);
			$('.comboBelong').combobox('select', data.userbelong);
			$('#userDetailTree').tree({
				url:'/userIndex/getTreeData/?data='+datatype,
				checkbox:true,
				lines:true,
				onLoadSuccess: function (a) {

					var rootnode = $('#userDetailTree').tree('getRoot');
					var children = $('#userDetailTree').tree('getChildren', rootnode.target);
					for (var i = 0; i < children.length; i++) {
						$('#userDetailTree').tree('collapse', children[i].target)
					}

					perway = data.permissionway
					var result = perway.split(",");
					for (var i = 0; i < result.length; i++) {
						var node = $('#userDetailTree').tree('find', result[i]);
						$('#userDetailTree').tree('check', node.target);
					}
					$('#userDetailTree').delegate('span[class ^= "tree-checkbox"]', 'click', function () {
						return false;
					})

				}

			});
}

// 修改
function ModifyMore() {
	var data = $("#userList").datagrid('getSelected');
	console.log(data.userid)
	dataid=data.userid;
	datatype=data.usertype;
		linkbutton_click('open_dialog',{dialog:'#userModifyDialog'});
			 $(".userType").each(function () {
					if($(this).val()==datatype)
						$(this).attr('checked',true);
				});
			$('.userid').val(data.userid);
			$('.username').val(data.username);
			$('.usertel').val(data.usertel);
			$('.usermail').val(data.usermail);
			$('.userother').val(data.userother);
			$('.comboBelong').combobox('select', data.userbelong);
			$('#userTreeModify').tree({
				url:'/userIndex/getTreeData/?data='+datatype,
				checkbox:true,
				lines:true,
				onLoadSuccess: function (a) {
					var rootnode = $('#userTreeModify').tree('getRoot');
					var children = $('#userTreeModify').tree('getChildren', rootnode.target);
					for (var i = 0; i < children.length; i++) {
						$('#userTreeModify').tree('collapse', children[i].target)
					}
					perway=data.permissionway
						var result=perway.split(",");
						for(var i=0;i<result.length;i++){
							var node = $('#userTreeModify').tree('find', result[i]);
							$('#userTreeModify').tree('check', node.target);
						}
    			 }
			});

}

//保存修改
function userInfoSave() {
		$('#userModifyForm').form('submit', {
		url: "/userIndex/userInfoSave/",
		onSubmit: function (t) {
			var nodes = $('#userTreeModify').tree('getChecked');
			var ids = '';
			for (var i in nodes) {
				ids += nodes[i].id + ',';
			}
			t.ids =ids.substr(0, ids.length - 1);
			return true
		},
		success: function (data) {
			$('#userModifyDialog').dialog('close');
			$('#userList').datagrid('reload');
		}
	});

}

//提交保存的东西
function savePer() {
	console.log(8888)
	$("#userForm").form('submit', {
		url: "/userIndex/passTreeData/",
		onSubmit: function (p) {
			var nodes = $('#userTree').tree('getChecked');
			var rows = $('#interList').datagrid('getSelections');
			var ids = '';
			var rowids='';
			for (var i in nodes) {
				ids += nodes[i].id + ',';
			}
			for (var i in rows) {
				rowids += rows[i].idapi + ',';
			}
			p.ids =ids.substr(0, ids.length - 1);
			p.rowids =rowids.substr(0, rowids.length - 1);
			return true
		},
		success: function (data) {
			$('#userForm').form('load',{username:'',userpwd:'',usertel:'',usermail:'',comboBelong:'',userother:''});
			$('#userTbas').tabs('disableTab', 1);
			// $('#userTree').tree('uncheck',node.target)
			$('#userDialog').dialog('close');
			$('#userList').datagrid('reload');

		}
	});
}

function formRet() {
	 $('.form_reset').form('reset')
}
//增加保存数据
// 	$("#userper_sub").linkbutton({
//         onClick:function(){
//             var userinfo=$("#userForm").serialize();
// 			var nodes = $('#userTree').tree('getChecked');
// 			var ids = '';
// 			for (var i in nodes) {
// 				ids += nodes[i].id + ',';
// 			}
// 			ids = 'ids=' + ids.substr(0, ids.length - 1);
// 			console.log(userinfo)
// 			console.log(ids)
// 			$.ajax({
// 				url:'/userIndex/passTreeData/',
// 				data:userinfo+'&'+ids,
// 				type:'get',
// 				datatype:'json',
// 				success:function(){
// 					$('#userDialog').dialog('close');
// 					$('#userList').datagrid('reload');
// 				}
//
// 			})
// 			}
//     })