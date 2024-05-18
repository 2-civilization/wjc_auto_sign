import { useState } from 'react';
import { TinyColor } from '@ctrl/tinycolor';
import { Form,message,Input,ConfigProvider,Button,Typography,Modal } from 'antd';
import { FireOutlined } from '@ant-design/icons';
import axios from 'axios';
const { Title,Link } = Typography;

export default function RegPage(props) {
    const colors1 = ['#6253E1', '#04BEFE'];
    const getHoverColors = (colors) =>
      colors.map((color) => new TinyColor(color).lighten(5).toString());
    const getActiveColors = (colors) =>
      colors.map((color) => new TinyColor(color).darken(5).toString());
  
    const [form] = Form.useForm();
    const [nowLoading,setNowLoading] = useState(false);
    const [isModalOpen,setModalOpen] = useState(false);

    async function checkAccount(){
      setNowLoading(true);
      form.validateFields()
        .then((val)=>{
          const setStep = props.setStep;
          const setFormData = props.setFormData;
          axios.post('/checkAccount',
            {
              account:val.account,
              pswd:val.pswd,
              email:val.email
            },{
              headers: {
                  'Content-Type': 'multipart/form-data'
                }
            })
            .then((res)=>{
              if(res.data.code === 'ok'){
                message.success(res.data.msg);
                setFormData({
                  account:val.account,
                  pswd:val.pswd,
                  email:val.email
                });
                setStep(1);
              }else{
                message.error(res.data.msg);
              }
              setNowLoading(false);
            }).catch((error)=>{
              setNowLoading(false);
              message.error("与服务器连接失败");
              console.log(error);
            })
          })
        .catch((err)=>{
          setNowLoading(false);
        });
    }
  
    return (
      <>
        <Title level={3}>填写账号</Title>
        <Form
          size='large'
          form={form}
        >
          <Form.Item
            label='账号'
            name='account'
            rules={[
              {
                required: true,
                message: '请输入正确的校芜优账号'
              },
              {
                min:11,
                max:11,
                message: '请输入正确的校芜优账号'
              }
            ]}
          >
            <Input placeholder='通常为你的学号'/>
          </Form.Item>
          <Form.Item
            label='密码'
            name='pswd'
            rules={[
              {
                required: true,
                message: '请输入正确的校芜优密码'
              }
            ]}
          >
            <Input.Password placeholder='推荐改成不常用密码后再填入' />
          </Form.Item>
          <Form.Item
            label='邮箱'
            name='email'
            rules={[
              {
                required: true,
                message: '请输入邮箱，用于通知签到'
              },
              {
                pattern:/^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$/,
                message:'请输入正确的邮箱'
              }
            ]}
          >
            <Input placeholder='推荐使用QQ邮箱'/>
          </Form.Item>
          <Form.Item>
            <ConfigProvider
              theme={{
                components: {
                  Button: {
                    colorPrimary: `linear-gradient(135deg, ${colors1.join(', ')})`,
                    colorPrimaryHover: `linear-gradient(135deg, ${getHoverColors(colors1).join(', ')})`,
                    colorPrimaryActive: `linear-gradient(135deg, ${getActiveColors(colors1).join(', ')})`,
                    lineWidth: 0,
                  },
                },
              }}
            >
              
              <Button block
                  type="primary"
                  icon={<FireOutlined />}
                  onClick={() =>{checkAccount()}}
                  loading={nowLoading}
                >
                  注册or更新
              </Button>
            </ConfigProvider>
          </Form.Item>
        </Form>
        <Link onClick={()=>{setModalOpen(true)}}>这是什么？点我查看说明</Link>
        <Modal
          title="使用说明"
          open={isModalOpen}
          onOk={() => {setModalOpen(false)}}
          onCancel={() => {setModalOpen(false)}}
        >
          <Typography>
            <p>这是一个在线的，可为你在每晚自动签到的脚本程序。</p>
            <p>它绕过了一些不必要的步骤，因此可以帮你更快地完成签到，甚至在他人校芜优打开失败的情况下。</p>
            <p>你需要填写你的校芜优的账号与密码，以及一个用于接收每晚签到信息的邮箱（很重要）。</p>
            <p>完成注册后，脚本会自动为你进行签到，你要做的只是关注下你的邮箱，确保签到成功即可。</p>
          </Typography>
        </Modal>
      </>
    );
}




