$(function() {
	$(".type").combobox({
		valueField: 'value',
		textField: 'text',
		data: [{
			"value": "1",
			"text": "普通文件本地上传"
		},
			{
			"value": "5",
			"text": "普通文件远程下载"
		},
			{
			"value": "2",
			"text": "数据库文件"
		}, {
			"value": "3",
			"text": "数据接口"
		}, {
			"value": "4",
			"text": "API接口"
		}],
	})
		$('#tt').tabs('disableTab', 1);

})

function collectLog() {
	window.open('/collectLog/','_blank');

}

function detailInfo() {
    var data = $("#sjyglList").datagrid('getSelections');
	if(data.length!=1) {
		$.messager.confirm('警告', '请选择一条数据', 'warning');
	}
	else {
		dataid = data[0].taskid
		if(data[0].tasktype=='1'){
			linkbutton_click('open_dialog', {dialog: '#fileDetailDialog'});
			$.get('/sjyglIndex/taskInfo/', {data: dataid}, function (ret) {
				$(".type").combobox("select", ret[0].filetype); //获取数据到input框
				$("#fileTasName").val(ret[0].taskname);
				$("#filetaskId").val(ret[0].taskid);
				$("#fileBelong").val(ret[0].belongto);
				$("#fileBelType").val(ret[0].belongtype);
				$("#fileTaskdom").val(ret[0].domid);
				$("#sfileName").val(ret[1].filename);
				$("#sfileNameWay").val(ret[1].fileway);
				$("#saveTypeFile").val(ret[1].sfiletype);
			})
		}
		if(data[0].tasktype=='2'){
			linkbutton_click('open_dialog', {dialog: '#sqlDetailDialog'});
			$.get('/sjyglIndex/taskInfo/', {data: dataid}, function (ret) {
				// alert(ret);
			    $(".type").combobox("select", ret[0].filetype);
				$("#sqlTasName").val(ret[0].taskname);
				$("#sqltaskId").val(ret[0].taskid);
				$("#sqlBelong").val(ret[0].belongto);
				$("#sqlBelType").val(ret[0].belongtype);
				$("#sqlTaskdom").val(ret[0].domid);
				$("#sqlfileName").val(ret[1].filename);
				$("#sqlfileNameWay").val(ret[1].fileway);
				$("#sqlsaveType").val(ret[1].tasktype);
			});
		}
		if(data[0].tasktype=='3') {
			linkbutton_click('open_dialog', {dialog: '#detailDialog'});
			// console.log(222)
			$.get('/sjyglIndex/taskInfo/', {data: dataid}, function (ret) {
				$(".type").combobox("select", ret[0].filetype);
				$("#tasName").val(ret[0].taskname);
				$("#taskId").val(ret[0].taskid);
				$("#belong").val(ret[0].belongto);
				$("#belType").val(ret[0].belongtype);
				$("#dom").val(ret[0].domid);
				$("#dataSoure").val(ret[1].sjyname);
				$("#dbName").val(ret[1].databasename);
				$("#dbType").val(ret[1].databasetype);
				$("#userName").val(ret[1].username);
				$("#userPwd").val(ret[1].pwd);
				$("#connIp").val(ret[1].fwqadress);
				$("#port").val(ret[1].dkname);
				$("#tableName").val(ret[1].tablename);
				$("#includeField").val(ret[1].ziduanname);
				$("#refreshChange").val(ret[0].refreshChange);

			});
		}
		if(data[0].tasktype=='4'){
			linkbutton_click('open_dialog', {dialog: '#apiDetailDialog'});
			$.get('/sjyglIndex/taskInfo/', {data: dataid}, function (ret) {
			    $(".type").combobox("select", ret[0].filetype);
				$("#apiTasName").val(ret[0].taskname);
				$("#taskIdApi").val(ret[0].taskid);
				$("#apiBelong").val(ret[0].belongto);
				$("#apiBelType").val(ret[0].belongtype);
				$("#aTaskdom").val(ret[0].domid);
				$("#urlAd").val(ret[1].url);
				$("#useMethod").val(ret[1].apitype);
				$("#param").val(ret[1].param);
				$("#byteAmout").val(ret[1].byteamount);
				$("#saveType").val(ret[1].filetype);
			});
		}
        if(data[0].tasktype=='5'){
			linkbutton_click('open_dialog', {dialog: '#DowfileDetailDialog'});
			$.get('/sjyglIndex/taskInfo/', {data: dataid}, function (ret) {
				// alert(ret);
				$(".type").combobox("select", ret[0].filetype);
				$("#downloadfileTasName").val(ret[0].taskname);
				$("#dowlfiletaskId").val(ret[0].taskid);
				$("#dowlfileBelong").val(ret[0].belongto);
				$("#dowlfileBelType").val(ret[0].belongtype);
				$("#dowlfileTaskdom").val(ret[0].domid);
				$("#dfileNameWay").val(ret[1].path);
				$("#downloadIp").val(ret[1].ip);
				$("#dUsername").val(ret[1].user);
				$("#downloadPwd").val(ret[1].pwd);
			})
		}
	}
}

// #普通文件上传
function fileChangeSave() {
	$('#changeFormFile').form('submit', {
		url: "/sjyglIndex/updateData/",

		onSubmit: function () {
			return true
		},
		success: function (data) {
			$('#fileDetailDialog').dialog('close');
			$('#sjyglList').datagrid('reload');
		}
	});
}


function closeFileDialog() {
	$('#fileDetailDialog').dialog('close');

}


// #数据库文件
function sqlChangeSave() {
	$('#changeFormSql').form('submit', {
		url: "/sjyglIndex/updateData/",

		onSubmit: function () {
			return true
		},
		success: function (data) {
			$('#sqlDetailDialog').dialog('close');
			$('#sjyglList').datagrid('reload');
		}
	});
}


function closeSqlDialog() {
	$('#sqlDetailDialog').dialog('close');

}


// #数据库接口
function changeSave() {
	$('#changeForm').form('submit', {
		url: "/sjyglIndex/updateData/",
		onSubmit: function () {
			return true
		},
		success: function (data) {
			$('#detailDialog').dialog('close');
			$('#sjyglList').datagrid('reload');
		}
	});
}


function closeDialog() {
	$('#detailDialog').dialog('close');

}

function testConn() {
	var data = '';
	$('#changeForm').form('submit', {
		url: "/sjyglIndex/testConn/",
		type:"GET",
		dataType:"JSON",
		onSubmit: function () {
			return true
		},
		success: function (data) {
			if (data==1) {
				$.messager.confirm('提示', '连接成功', 'warning');
			}
			else{

				$.messager.confirm('提示', '连接失败，请重新配置', 'warning');
			}
		}

	});
}

// #API接口
function apiChangeSave() {
	$('#changeFormA').form('submit', {
		url: "/sjyglIndex/updateData/",

		onSubmit: function () {
			return true
		},
		success: function (data) {
			$('#apiDetailDialog').dialog('close');
			$('#sjyglList').datagrid('reload');
		}
	});
}


function closeApiDialog() {
	$('#detailDialog').dialog('close');

}


// #普通文件下载
function dowfileChangeSave() {
	$('#changeFormFileDow').form('submit', {
		url: "/sjyglIndex/updateData/",

		onSubmit: function () {
			return true
		},
		success: function (data) {
			$('#DowfileDetailDialog').dialog('close');
			$('#sjyglList').datagrid('reload');
		}
	});
}

function dowcloseFileDialog() {
	$('#DowfileDetailDialog').dialog('close');

}

//点击修改执行频率

function refreshModify_btn_sure(){

			var refreshModifyForm = $("#refreshModify_form").serialize();
			var changeForm= $('#changeForm').serialize();
			$.ajax({
				url:'/sjyglIndex/updataRefesh/',
				data:refreshModifyForm+'&'+changeForm,
				type:'get',
				gatatype:'json',
				success:function (ret) {
					$('#tt').tabs('disableTab', 1);
					$('#tt').tabs('select', 0);
					var tab = $('#tt').tabs('getSelected');
					$('#sjyglList').datagrid('reload');
					$('#refreshChange').val(ret)
				}
			})


}


