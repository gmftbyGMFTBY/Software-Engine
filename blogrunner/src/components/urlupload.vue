<template>
  <el-container class='search'>
    <el-form
      v-loading.fullscreen.lock='loading'
      element-loading-text="拼命加载中"
      element-loading-spinner="el-icon-loading"
      element-loading-background="rgba(0, 0, 0, 0.8)"
      ref="form" :model="form" label-width="80px">
      <el-form-item>
        <el-input v-model="value" placeholder="请输入检测的URL"></el-input>
      </el-form-item>
      <el-form-item>
        <el-rate type="primary" v-model=grade></el-rate>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="upload">上传</el-button>
      </el-form-item>
    </el-form>
  </el-container>
</template>
<script>
export default {
  data () {
    return {
      value: '',
      grade: 0
    }
  },
  methods: {
    upload () {
      var self = this
      self.data = JSON.stringify({'grade': self.grade, 'url': self.value})
      self.$http.post('http://127.0.0.8:8888/urlupload', self.data)
      .then(function (response) {
        console.log(response)
        self.result = response.data['result']
        console.log(self.result)
        if (self.result === -1) {
          self.$message.error('抱歉，请键入CSDN博文地址')
        } else {
          self.$message({
            message: '上传成功，预计博文阅读量为' + self.result.toString(),
            type: 'success'
          })
        }
        // 之后的返回的关于网页的信息的评价的逻辑
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  }
}
</script>
<style>
body {
  background-image: url('../assets/website.jpg');
  background-size:cover;
  width:100%;
  height:100%;
}
.search {
  padding: 180px;
  width:60%;
  margin: auto;
} 
</style>
