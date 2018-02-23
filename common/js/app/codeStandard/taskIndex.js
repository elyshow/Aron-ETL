

$(function () {
	$("#codestandardclass").combobox({
		valueField: 'label',
		textField: 'value',
		data: [{
			label: '1',
			value: '国标'
		},{
			label: '2',
			value: '部标'
		},{
			label: '3',
			value: '省标'
		},{
			label:'4',
			value: '扩展标准'
		},{
			label:'5',
			value: '未分类'
		}],
})
})

$(function () {
	$("#resourceproperty").combobox({
		valueField: 'label',
		textField: 'value',
		data: [{
			label: '1',
			value: '基本信息'
		},{
			label: '2',
			value: '关系信息'
		},{
			label: '3',
			value: '图片影像信息'
		},{
			label:'4',
			value: '生物特征信息'
		},{
			label:'5',
			value: '行政管理行为'
		},{
			label:'6',
			value: '侦查调查行为'
		},{
			label:'7',
			value: '违法犯罪管理行为'
		},{
			label:'8',
			value: '内部管理行为'
		}],
	})
})

$(function () {

	$('#myTab').tabs({
		clicks:[0,1,2,3,4,5],
		onSelect:function (title, index) {
			if($(this).tabs('options').clicks[index]==0) {
				loadDataList({
					list: '#all',
					url: '/standardIndex/taskIndex/getDataList/',
					type: index,
					toolbar: '#cleanRulesToolBar',
				});
			}
			if($(this).tabs('options').clicks[index]==1) {
				loadDataList({
					list: '#country',
					url: '/standardIndex/taskIndex/getDataList/',
					type: index,
					toolbar: '#cleanRulesToolBar',
				});
			}
			if($(this).tabs('options').clicks[index]==2) {
				loadDataList({
					list: '#branch',
					url: '/standardIndex/taskIndex/getDataList/',
					type: index,
					toolbar: '#cleanRulesToolBar',
				});

			}
			if($(this).tabs('options').clicks[index]==3) {
				loadDataList({
					list: '#province',
					url: '/standardIndex/taskIndex/getDataList/',
					type: index,
					toolbar: '#cleanRulesToolBar',
				});

			}
			if($(this).tabs('options').clicks[index]==4) {
				loadDataList({
					list: '#extra',
					url: '/standardIndex/taskIndex/getDataList/',
					type: index,
					toolbar: '#cleanRulesToolBar',
				});

			}
			if($(this).tabs('options').clicks[index]==5) {
				loadDataList({
					list: '#unclassified',
					url: '/standardIndex/taskIndex/getDataList/',
					type: index,
					toolbar: '#cleanRulesToolBar',
				});

			}
			}
	}).tabs('unselect',0).tabs('select',0)
})



function loadDataList(obj) {
	window.type = obj.type;
	$(obj.list).datagrid({
		url:obj.url,
		queryParams:{
			type:obj.type,
		},
		method:'post',
		striped:true,
		autoRowHeight:true,
		toolbar:obj.toolbar,
		columns:[[
			{field:'checkbox',checkbox:true},
			// {field:'id',title:'id',width:'10%',},
			{field:'codename',title:'代码名称',width:'20%',},
			{field:'standardnum',title:'标准编号',width:'20%',},
			{field:'codetable',title:'代码表',width:'15%',},
			{field:'datasource',title:'数据源',width:'15%',},
			{field:'registertime',title:'注册时间',width:'15%',},
			{field:'codesetname',title:'操作',width:'15%',formatter:func},
        ]], onLoadSuccess:function(){
             // 图标
           $('.stateDetail').linkbutton({
					iconCls: 'icon-more'
				});
    },

	})
	$("#businessclass").combobox({
	url:'/standardIndex/taskIndex/sjygl/',
	textField:'codename',
	valueField:'codeid',
    });

	 $('#dataSearch').searchbox({
        prompt:'请输入代码名称',
        height:24,
        width:200,
        searcher:function(v,n){
           $('#all').datagrid('load', {condition:v,type:0})
           $('#country').datagrid('load', {condition:v,type:1})
           $('#branch').datagrid('load', {condition:v,type:2})
           $('#province').datagrid('load', {condition:v,type:3})
           $('#extra').datagrid('load', {condition:v,type:4})
           $('#unclassified').datagrid('load', {condition:v,type:5})
        }
    })
}


function func(v, r, i) {
		return 	'<a data-hover="查看详情" title="查看详情" class="stateDetail" href="javascript:detailTask(' + i + ');" data-options="" ></a>'
}
   
function detailTask(i){
		switch(type){
			case 0 :
				var dataGrid = $('#all')
				break;
			case 1 :
				var dataGrid = $('#country')
				break;
			case 2 :
				var dataGrid = $('#branch')
				break;
			case 3 :
				var dataGrid = $('#province')
				break;
			case 4 :
				var dataGrid = $('#extra')
				break;
			case 5 :
				var dataGrid = $('#unclassified')
				break;
			default:
				$.messager.alert('错误', '选项卡不存在', 'error');
				return;
				break
		}
		
		if(dataGrid.datagrid('getSelections').length > 1){
			$.messager.alert('错误', '一次只能查看一条记录', 'error');
			return;
		}
		var	list = dataGrid.datagrid('getRows')[i];

		var codetableDetailval = list.codetable
		$("#quoteDetail").datagrid({
			url:'/standardIndex/taskIndex/detilList/',
			queryParams: {
				data:codetableDetailval
			},
			columns:[[
				{field:'identifier',title:'内部标识符',width:'12%'},
				{field:'inseridentifier',title:'中文简拼',width:'12%'},
				{field:'object',title:'对象',width:'17%'},
				{field:'datatype',title:'数据类型',width:'8%'},
				{field:'datafrom',title:'数据来源',width:'12%'},
				{field:'remark',title:'特征词',width:'8%'},
				{field:'cnname',title:'同义名称',width:'15%'},
				{field:'state',title:'状态',width:'5%'},
			]]
		});

		 var id = list.id
		 linkbutton_click('open_dialog', {dialog: '#detailTaskDialog'});
		 $.post('/standardIndex/taskIndex/DetailTask/', {datas: id}, function (yeat) {
		 console.log(yeat[0]);
		 $("#codenameDetail").val(yeat[0].codenameDetail);
		 $("#standardnumDetail").val(yeat[0].standardnumDetail);
		 $("#codetableDetail").val(yeat[0].codetableDetail);
		 $("#datasourceDetail").val(yeat[0].datasourceDetail);
		 $("#registertimeDetail").val(yeat[0].registertimeDetail);
		 $("#businessclassDetail").val(yeat[0].businessclassDetail);
		     if(yeat[0].structuretypeDetail==1){
				  var structuretypeDetailval='普通列表'
			 }else if(yeat[0].structuretypeDetail=2){
				  structuretypeDetailval='父级字段'
			 }else if(yeat[0].structuretypeDetail==3){
				  structuretypeDetailval='分段编号'
			 }else if(yeat[0].structuretypeDetail==4){
				  structuretypeDetailval='分段补零'
			 }
		 $("#structuretypeDetail").val(structuretypeDetailval);
		
			 if(yeat[0].codestandardclassDetail==1){
				  var codestandardclassDetailval='国标'
			 }else if(yeat[0].codestandardclassDetail==2){
				 codestandardclassDetailval='部标'
			 }else if(yeat[0].codestandardclassDetail==3){
				 codestandardclassDetailval='省标'
			 }else if(yeat[0].codestandardclassDetail==4){
				 codestandardclassDetailval='扩展标准'
			 }else if(yeat[0].codestandardclassDetail==5){
				 codestandardclassDetailval='未分类'
			 }
		 $("#codestandardclassDetail").val(codestandardclassDetailval);
		 //     if(yeat[0].resourcepropertyDetail==1){
			// 	 var resourcepropertyDetailval = '基本信息'
			//  }else if(yeat[0].resourcepropertyDetail==2){
			// 	 resourcepropertyDetailval = '关系信息'
			//  }else if(yeat[0].resourcepropertyDetail==3){
			// 	 resourcepropertyDetailval = '图片影像信息'
			//  }else if(yeat[0].resourcepropertyDetail==4){
			// 	 resourcepropertyDetailval = '生物特征信息'
			//  }else if(yeat[0].resourcepropertyDetail==5){
			// 	 resourcepropertyDetailval = '行政管理行为'
			//  }else if(yeat[0].resourcepropertyDetail==6){
			// 	 resourcepropertyDetailval = '侦查调查行为'
			//  }else if(yeat[0].resourcepropertyDetail==7){
			// 	 resourcepropertyDetailval = '违法犯罪管理行为'
			//  }else if(yeat[0].resourcepropertyDetail==8){
			// 	 resourcepropertyDetailval = '内部管理行为'
			//  }
		 // $("#resourcepropertyDetail").val(resourcepropertyDetailval);
		 // $("#typeDetail").val(yeat[0].typeDetail);
		 })
}





function editCleaningRules(){
	    $('input[name="save_type"]').val('edit')
	    var list =''
	    if(type == 0){
			list = $('#all').datagrid('getSelections');
		}else if(type == 1){
			list = $('#country').datagrid('getSelections');
		}else if(type == 2){
			list = $('#branch').datagrid('getSelections');
		}else if(type == 3){
			list = $('#province').datagrid('getSelections');
		}else if(type == 4){
			list = $('#extra').datagrid('getSelections');
		}else if(type == 5){
			list = $('#unclassified').datagrid('getSelections');
		}

        if(list.length == 0){
            $.messager.alert('错误',"请至少选择一条数据修改",'error')
        }else if(list.length > 1){
            $.messager.alert('错误',"一次只能修改一条数据",'error')
        }else{
			linkbutton_click('open_dialog' ,{dialog: '#mydialog'});
			id=list[0].id
			$.post('/standardIndex/taskIndex/changeList/',{data:id},function (read) {
				console.log(read[0]);
				$('#id').val(read[0].id);
				$("#codename").val(read[0].codename).validatebox('validate');
				$("#standardnum").val(read[0].standardnum).validatebox('validate');
				$("#codetable").val(read[0].codetable).validatebox('validate');
				$("#datasource").val(read[0].datasource).validatebox('validate');
				$("#other").val(read[0].other);
				$(".structuretype").each(function () {
					if($(this).val()==read[0].structuretype)
						$(this).attr('checked',true) ;
				})
				$("#businessclass").combobox('select',read[0].businessclass).validatebox('validate');
				$("#codestandardclass").combobox('select',read[0].codestandardclass);
				$("#resourceproperty").combobox('select',read[0].resourceproperty);
			})
        }
}

function addCleaningRules(){
	   $('input[name="save_type"]').val('add')
	   $('#busForm').form('reset');
	    linkbutton_click('open_dialog' ,{dialog: '#mydialog'});
}
  
function saveRules(){
	$("#busForm").form('submit', {
		url: "/standardIndex/taskIndex/save/",
		param:{
            type: 1,
        },
		onSubmit: function () {
			console.log($(this).form('validate'));
			return $(this).form('validate');
		},
		success: function (data) {
			$("#mydialog").dialog('close');
			$("#all").datagrid('reload');
			$("#country").datagrid('reload');
			$("#branch").datagrid('reload');
			$("#province").datagrid('reload');
			$("#extra").datagrid('reload');
			$("#unclassified").datagrid('reload');
		}
	});
	
}

function delCleaningRules(){
	     console.log(type)
	     var list =''
	   if(type == 0){
		    list = $('#all').datagrid('getSelections');
	      }else if(type == 1){
		    list = $('#country').datagrid('getSelections');
	      }else if(type == 2){
		    list = $('#branch').datagrid('getSelections');
	      }else if(type == 3){
		    list = $('#province').datagrid('getSelections');
	      }else if(type == 4){
		    list = $('#extra').datagrid('getSelections');
	      }else if(type == 5){
		    list = $('#unclassified').datagrid('getSelections');
	      }
		if (list.length == 0){
			$.messager.alert('错误','请至少选择一条数据删除','error')
		}else{
			$.messager.confirm('确认删除框','是否确定删除选中记录?',function(ok){
			if(ok){
				var names = '';
				for (var i in list){
					names += list[i].id + ',';
				  }
				names = names.substr(0, names.length -1);
				console.log(names)
				$.post('/standardIndex/taskIndex/delList/',{data:names},function(msg){
					$("#all").datagrid('reload');
					$("#country").datagrid('reload');
					$("#branch").datagrid('reload');
					$("#province").datagrid('reload');
					$("#extra").datagrid('reload');
					$("#unclassified").datagrid('reload');
					})
				 }

		})
			
		}
}
//导表
function insetCleaningRules() {
	$('#all').datagrid({
	     url: "/standardIndex/taskIndex/insertTable/",
		success: function (data) {
			$("#all").datagrid('reload');
			$("#country").datagrid('reload');
			$("#branch").datagrid('reload');
			$("#province").datagrid('reload');
			$("#extra").datagrid('reload');
			$("#unclassified").datagrid('reload');
		}
		
	})
}

// $(function () {
// 	$("#quoteDetail").datagrid({
// 		url:'/taskIndex/detilList/',
// 		columns:[[
// 			{field:'identifier',title:'identifier',width:'10%'},
// 			{field:'inseridentifier',title:'inseridentifier',width:'10%'},
// 			{field:'object',title:'object',width:'10%'},
// 			{field:'datatype',title:'datatype',width:'10%'},
// 			{field:'datafrom',title:'datafrom',width:'10%'},
// 			{field:'remark',title:'remark',width:'10%'},
// 			{field:'cnname',title:'cnname',width:'10%'},
// 			{field:'state',title:'state',width:'10%'},
// 			{field:'tabtype',title:'tabtype',width:'10%'},
// 		]]
// 	})
// })