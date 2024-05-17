import { useState } from 'react';
import { TinyColor } from '@ctrl/tinycolor';
import { Form, message,Input,ConfigProvider,Button,Typography } from 'antd';
import { FireOutlined } from '@ant-design/icons';
const { Title } = Typography;

export default function RegPage(props) {
    const colors1 = ['#6253E1', '#04BEFE'];
    const getHoverColors = (colors) =>
      colors.map((color) => new TinyColor(color).lighten(5).toString());
    const getActiveColors = (colors) =>
      colors.map((color) => new TinyColor(color).darken(5).toString());
  
    const [form] = Form.useForm();
    const [nowLoading,setNowLoading] = useState(false);
    
    async function checkAccount(){
      setNowLoading(true);
      try{
        const val = await form.validateFields();
        if(val.account && val.pswd && val.email){
          if(await accountOnlineCheck(val.account,val.pswd)){
            message.info('账号验证成功！');
            props.setStep(1);
            props.setFromData({
              username:val.account,
              password:val.pswd,
              email:val.email
            });
          }else{
            message.error('账号或密码错误');
          }
          setNowLoading(false);
        }
      }catch(e){
        setNowLoading(false);
        console.log(e);
      }
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
                  onClick={checkAccount}
                  loading={nowLoading}
                >
                  注册or更新
              </Button>
            </ConfigProvider>
          </Form.Item>
        </Form>
      </>
    );
  }

  async function accountOnlineCheck(account,pswd){
    const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay));
    await sleep(3000);
    return true;
  }