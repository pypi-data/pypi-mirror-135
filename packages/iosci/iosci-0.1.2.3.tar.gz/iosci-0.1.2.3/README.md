# ios 自动修改podfile组件版本号，支持批量修改
如果podfile中不存在组件aaa，则添加到podfile第一个target中,如果有:configurations=>['Debug']则保留
f_podfile = '/Users/lch/Desktop/Podfile'

组件统一更改版本号
update_component_with_newversion(f_podfile, ['aaa:1.0','bbb:2.0'], 'master')

组件统一更改成git指向
update_component_with_newversion(f_podfile, ['aaa:https://github.com/aaa.git','bbb:https://github.com/bbb.git'], 'master')

## podfile转为model对象
      podfile = '/Users/lch/Documents/z/proj/Podfile'
      podfile_model = CIPodfileParse.getPodfileModel(podfile)
      print(podfile_model)

## 验证字符串是不是版本号
    isversion = CIVersionManager.isVersion('1.1.2')
    print(isversion)

## 执行shell脚本
    # os_system('cat aaa')
    (status, msg) = os_popen('xcodebuild  aaa > /dev/null')
    print(status)
    print(msg)

'''
install! 'cocoapods', :deterministic_uuids => false
source 'https://gitlab.com/wireless/ios/static.git'
platform :ios, '9.0'
target 'HHYProject' do
#登录
  pod 'aaaa', '1.10' , :configurations=>['Debug']

  pod 'bbbb', '1.0' , :configurations=>['Debug']

  pod 'cccc', :git => 'https://github.com/sdweb.git' , :branch => 'lich',  :configurations=>['Debug']

  pod 'ddddd', :git=>'https://gitlab.com/ddd.git' , :branch=>'feature_20211221_cleanConfirmation',  :configurations=>['Debug']

end
 
post_install do |installer_representation|
  installer_representation.pods_project.targets.each do |target|
    target.build_configurations.each do |config|
      config.build_settings['APPLICATION_EXTENSION_API_ONLY'] = 'NO'
    end
  end
end

'''