local t = {}


--[[
	android gpu 评分
		基于 GFXBench@notebookcheck.net 评分

        
local android_gpu_score =
{
	["Adreno (TM) 304"]=5.2,
	["Adreno (TM) 306"]=5.25,
	["Adreno (TM) 308"]=7.6,
	["Adreno (TM) 330"]=24,
	["Adreno (TM) 405"]=14,
	["Adreno (TM) 418"]=34,
	["Adreno (TM) 420"]=41.35,
	["Adreno (TM) 430"]=49,
	["Adreno (TM) 504"]=11,
	["Adreno (TM) 505"]=17,
	["Adreno (TM) 506"]=23,
	["Adreno (TM) 508"]=30,
	["Adreno (TM) 509"]=36,
	["Adreno (TM) 510"]=31,
	["Adreno (TM) 512"]=50,
	["Adreno (TM) 530"]=88,
	["Adreno (TM) 540"]=111.5,
	["Adreno (TM) 610"]=36,
	["Adreno (TM) 612"]=41,
	["Adreno (TM) 616"]=65,
	["Adreno (TM) 618"]=84,
	["Adreno (TM) 619"]=90,
	["Adreno (TM) 619L"]=73,
	["Adreno (TM) 620"]=91,
	["Adreno (TM) 630"]=150,
	["Adreno (TM) 642"]=153,
	["Adreno (TM) 640"]=166,
	["Adreno (TM) 650"]=203.5,
	["Adreno (TM) 660"]=268,
	["Adreno (TM) 730"]=437.5,
	["Mali-400"]=4.15,
	["Mali-400 MP2"]=4.25,
	["Mali-400 MP4"]=4,
	["Mali-450 MP4"]=10.05,
	["Mali-G51 MP4"]=39,
	["Mali-G52 2EEMC2"]=35,
	["Mali-G52 MP2"]=39,
	["Mali-G52 MP6"]=87,
	["Mali-G71 MP2"]=22,
	["Mali-G71 MP20"]=105,
	["Mali-G71 MP8"]=73.5,
	["Mali-G72 MP12"]=118,
	["Mali-G72 MP18"]=145,
	["Mali-G72 MP3"]=38,
	["Mali-G76 MP10"]=119.5,
	["Mali-G76 MP12"]=96.5,
	["Mali-G76 MP16"]=151.5,
	["Mali-G76 MP4"]=80,
	["Mali-G77 MP11"]=199,
	["Mali-G77 MP9"]=177,
	["Mali-G78 MP14"]=154,
	["Mali-G57 MP5"]=115,
	["Mali-G57 MP6"]=112,
	["Mali-G57 MP4"]=86,
	["Mali-G57 MP3"]=79,
	["Mali-G57 MP2"]=61,
	["Mali-T604 MP4"]=12.4,
	["Mali-T624"]=14.2,
	["Mali-T628 MP4"]=12,
	["Mali-T628 MP6"]=22.8,
	["Mali-T720"]=5.95,
	["Mali-T720 MP2"]=9.55,
	["Mali-T720 MP4"]=12,
	["Mali-T760 MP2"]=14.6,
	["Mali-T760 MP4"]=16,
	["Mali-T760 MP6"]=31,
	["Mali-T760 MP8"]=53.5,
	["Mali-T830"]=12,
    ["Mali-T830 MP1"]=12,
	["Mali-T830 MP2"]=18.5,
	["Mali-T830 MP3"]=34,
	["Mali-T860 MP2"]=17,
	["Mali-T880 MP12"]=82,
	["Mali-T880 MP2"]=24,
	["Mali-T880 MP4"]=39,
	["PowerVR Rogue G6430"]=27.9,
	["PowerVR GM9446"]=57,
	["PowerVR GM8320"]=19,
	["PowerVR GM8300"]=14,
	["PowerVR GM8100"]=6,
	["PowerVR Rogue GE8320"]=19,
}
]]

--根据https://www.notebookcheck.net/ARM-Mali-G78-MP22-GPU-Benchmarks-and-Specs.573765.0.html
--分档0最高档 1一档 2二档 3最低档
local android_gpu_score =
{
	["Adreno (TM) 200"]=3,
	["Adreno (TM) 203"]=3,
	["Adreno (TM) 205"]=3,
	["Adreno (TM) 220"]=3,
	["Adreno (TM) 225"]=3,
	["Adreno (TM) 302"]=3,
	["Adreno (TM) 304"]=3,
	["Adreno (TM) 305"]=3,
	["Adreno (TM) 306"]=3,
	["Adreno (TM) 308"]=3,
	["Adreno (TM) 320"]=3,
	["Adreno (TM) 330"]=3,
	["Adreno (TM) 405"]=3,
	["Adreno (TM) 418"]=2,
	["Adreno (TM) 420"]=1,
	["Adreno (TM) 430"]=1,
	["Adreno (TM) 504"]=3,
	["Adreno (TM) 505"]=3,
	["Adreno (TM) 506"]=3,
	["Adreno (TM) 508"]=3,
	["Adreno (TM) 509"]=3,
	["Adreno (TM) 510"]=2,
	["Adreno (TM) 512"]=2,
	["Adreno (TM) 530"]=1,
	["Adreno (TM) 540"]=1,
	["Adreno (TM) 610"]=2,
	["Adreno (TM) 612"]=2,
    ["Adreno (TM) 613"]=2, --没找到rank
	["Adreno (TM) 616"]=2,
	["Adreno (TM) 618"]=2,
	["Adreno (TM) 619"]=2,
	["Adreno (TM) 619L"]=2,
	["Adreno (TM) 620"]=1,
	["Adreno (TM) 630"]=1, --没找到rank
	["Adreno (TM) 640"]=1,
    ["Adreno (TM) 642"]=1,
    ["Adreno (TM) 642L"]=1, 
	["Adreno (TM) 643"]=1,
    ["Adreno (TM) 644"]=1,
	["Adreno (TM) 650"]=0,
	["Adreno (TM) 660"]=0,
	["Adreno (TM) 662"]=1,
    ["Adreno (TM) 710"]=0, 
	["Adreno (TM) 725"]=0,
    ["Adreno (TM) 730"]=0,
    ["Adreno (TM) 740"]=0, 
    ["Adreno (TM) 750"]=0,

	["Mali-200"]=3,
	["Mali-400"]=3, 
	["Mali-400 MP"]=3, 
	["Mali-400 MP2"]=3, 
	["Mali-400 MP4"]=3, 
	["Mali-450 MP4"]=3,

	["Mali-G51 MP4"]=2,
	["Mali-G52 MP1"]=1,
	["Mali-G52 MP2"]=1,
	["Mali-G52 MP6"]=1,
	["Mali-G52 2EEMC2"]=2,
	
    ["Mali-G57 MP5"]=1, 
	["Mali-G57 MP6"]=1, 
	["Mali-G57 MP4"]=1, 
	["Mali-G57 MP3"]=1, 
	["Mali-G57 MP2"]=2, 
    ["Mali-G57 MP1"]=2, 
	["Mali-G57 MC5"]=2, 
	["Mali-G57 MC4"]=2, 
	["Mali-G57 MC3"]=2, 
	["Mali-G57 MC2"]=3, 

	["Mali-G68 MP2"]=1,
    ["Mali-G68 MP4"]=1,
	["Mali-G68 MC4"]=2,
	["Mali-G68 MP5"]=1,
    
    ["Mali-G71 MP2"]=1, 
	["Mali-G71 MP8"]=1,
	["Mali-G71 MP20"]=1,

	["Mali-G72 MP3"]=1,
	["Mali-G72 MP12"]=1,
	["Mali-G72 MP18"]=1,
	
	["Mali-G76 MP4"]=1,
	["Mali-G76 MP5"]=1, --没找到rank
	["Mali-G76 MP10"]=1,
	["Mali-G76 MP12"]=1,
	["Mali-G76 MP16"]=1,
  

	["Mali-G77 MP11"]=1,
	["Mali-G77 MP9"]=1,
	["Mali-G77 MC9"]=2,
    ["Mali-G77 MP8"]=2, --没找到rank
	["Mali-G78 MP14"]=0,
    ["Mali-G78 MP20"]=0,
    ["Mali-G78 MP22"]=0,
	["Mali-G78 MP24"]=0,

    ["Mali-G610"]=1, --没找到rank
	["Mali-G610 MP3"]=1,
	["Mali-G610 MP4"]=1,
	["Mali-G610 MP6"]=1,
	["Mali-G610 MC6"]=1,
    ["Mali-G615 MP6"]=0,
	["Mali-G710 MP7"]=0,
	["Mali-G710 MP10"]=0,
	["Mali-G710 MC10"]=0,
	["Mali-G715 MP7"]=0,

	["Mali-T604 MP4"]=3, 
	["Mali-T624"]=3, 
	["Mali-T628 MP4"]=3, 
	["Mali-T628 MP6"]=3, 
	["Mali-T720"]=3, 
	["Mali-T720 MP2"]=3, 
	["Mali-T720 MP4"]=3, 
	
	["Mali-T760 MP2"]=3, 
	["Mali-T760 MP4"]=3,
	["Mali-T760 MP6"]=2,
	["Mali-T760 MP8"]=1,

	["Mali-T830"]=3,--没找到rank
    ["Mali-T830 MP1"]=3,
	["Mali-T830 MP2"]=3,
	["Mali-T830 MP3"]=2,
	["Mali-T860 MP2"]=3,
	
	["Mali-T880 MP2"]=3,
	["Mali-T880 MP4"]=3,
	["Mali-T880 MP12"]=1,

	["PowerVR Rogue G6430"]=3, --没找到rank
	["PowerVR GM9446"]=1,
	["PowerVR GM8320"]=3, 
	["PowerVR GM8300"]=3, 
	["PowerVR GM8100"]=3, 
	["PowerVR Rogue GE8320"]=3, 
    ["PowerVR GE8322"]=3,
    ["PowerVR GE8320"]=3,
	["PowerVR GE8300"]=3,
	["PowerVR GE8100"]=3,
    ["PowerVR 7XTP-MT4"]=3, --没找到rank
	["PowerVR GXA6850"]=1,
	["PowerVR GX6250"]=3,
	["PowerVR GX6450"]=1,
	["PowerVR G6200"]=3,
	["PowerVR G6400"]=3,
	["PowerVR G6430"]=3,
	

    ["Maleoon 910"]=1, --131.5(麒麟9000S)
    ["Xclipse 920"]=0,
	["Xclipse 940"]=0,
    ["Immortalis-G715 MC11"]=0, --321.8(天玑9200+)
    ["Immortalis-G720 MC12"]=0,
	["IMG BXM-8-256"]=1,
	["SGX554MP4"]=3,
	["SGX543MP4"]=3,
	["SGX543MP3"]=3,
	["SGX543MP2"]=3,
	["SGX545"]=3,
	["SGX544MP2"]=3,
	["SGX544"]=3,
	["SGX540"]=3,
	["SGX535"]=3,
	["SGX531"]=3,
	["SGX530"]=3,

	["Vivante GC7000UL"]=3,
	["Vivante GC4000"]=3,
	["Vivante GC1000+ Dual-Core"]=3,
	["Vivante GC800"]=3,
}

local RankEnum = 
{
    Low0 = 3, --最低档
    Low1 = 2, --低档
    Mid  = 1, --中档
    High = 0, --高档
}

t.isLowest = false

function t:SetParamLowest()
    print("GPU SetParamLowest")
    local gameInstance = gameInstance
    local ExecuteConsoleCommand = UE.UKismetSystemLibrary.ExecuteConsoleCommand
    do
        ExecuteConsoleCommand(gameInstance,"r.MobileContentScaleFactor 0.7")
        --ExecuteConsoleCommand(gameInstance,"r.ScreenPercentage 30")
        ExecuteConsoleCommand(gameInstance,"sg.ViewDistanceQuality 0")
        ExecuteConsoleCommand(gameInstance,"sg.AntiAliasingQuality 0")
        ExecuteConsoleCommand(gameInstance,"sg.ShadowQuality 0")
        ExecuteConsoleCommand(gameInstance,"sg.PostProcessQuality 0")
        ExecuteConsoleCommand(gameInstance,"sg.TextureQuality 0")
        ExecuteConsoleCommand(gameInstance,"sg.EffectsQuality 0")
        ExecuteConsoleCommand(gameInstance,"sg.FoliageQuality 0")
    end

    do
        ExecuteConsoleCommand(gameInstance,"r.AllowOcclusionQueries 1")
        ExecuteConsoleCommand(gameInstance,"r.RHIThread.Enable 0")
    end

    if true then 
        ExecuteConsoleCommand(gameInstance,"ShowFlag.VisualizeSSR 0")
        ExecuteConsoleCommand(gameInstance,"ShowFlag.ScreenSpaceReflections 0")
        ExecuteConsoleCommand(gameInstance,"ShowFlag.PostProcessing 0")
        ExecuteConsoleCommand(gameInstance,"ShowFlag.LightFunctions 0")
        ExecuteConsoleCommand(gameInstance,"ShowFlag.IndirectLightingCache 0")
        ExecuteConsoleCommand(gameInstance,"ShowFlag.AntiAliasing 0")
        ExecuteConsoleCommand(gameInstance,"r.SSR.MaxRoughness 0.1")
        ExecuteConsoleCommand(gameInstance,"ShowFlag.Bloom 0")
    end

    if true then
        --ExecuteConsoleCommand(gameInstance,"ShowFlag.Decals 0")
        ExecuteConsoleCommand(gameInstance,"ShowFlag.DynamicShadows 0")
        ExecuteConsoleCommand(gameInstance,"ShowFlag.Fog 0")
        ExecuteConsoleCommand(gameInstance,"ShowFlag.InstancedFoliage 0")
        ExecuteConsoleCommand(gameInstance,"ShowFlag.VolumetricLightmap 0")
    end
end

function t:SetParamLow()
    print("GPU SetParamLow")
    local gameInstance = gameInstance
    local ExecuteConsoleCommand = UE.UKismetSystemLibrary.ExecuteConsoleCommand
    do
        ExecuteConsoleCommand(gameInstance,"r.MobileContentScaleFactor 0.8")
        ExecuteConsoleCommand(gameInstance,"sg.ViewDistanceQuality 0")
        ExecuteConsoleCommand(gameInstance,"sg.AntiAliasingQuality 0")
        ExecuteConsoleCommand(gameInstance,"sg.ShadowQuality 0")
        ExecuteConsoleCommand(gameInstance,"sg.PostProcessQuality 0")
        ExecuteConsoleCommand(gameInstance,"sg.TextureQuality 0")
        ExecuteConsoleCommand(gameInstance,"sg.EffectsQuality 0")
        ExecuteConsoleCommand(gameInstance,"sg.FoliageQuality 0")
    end
end

function t:SetParamMid()
    print("GPU SetParamMid")
    local ExecuteConsoleCommand = UE.UKismetSystemLibrary.ExecuteConsoleCommand
    local gameInstance = gameInstance
    do
        ExecuteConsoleCommand(gameInstance,"r.MobileContentScaleFactor 1")
        ExecuteConsoleCommand(gameInstance,"sg.ViewDistanceQuality 1")
        ExecuteConsoleCommand(gameInstance,"sg.AntiAliasingQuality 1")
        ExecuteConsoleCommand(gameInstance,"sg.ShadowQuality 1")
        ExecuteConsoleCommand(gameInstance,"sg.PostProcessQuality 1")
        ExecuteConsoleCommand(gameInstance,"sg.TextureQuality 1")
        ExecuteConsoleCommand(gameInstance,"sg.EffectsQuality 1")
        ExecuteConsoleCommand(gameInstance,"sg.FoliageQuality 1")
    end
end

function t:SetParamHigh()
    print("GPU SetParamHigh")
    local ExecuteConsoleCommand = UE.UKismetSystemLibrary.ExecuteConsoleCommand
    local gameInstance = gameInstance
    do
        ExecuteConsoleCommand(gameInstance,"r.MobileContentScaleFactor 1")
        ExecuteConsoleCommand(gameInstance,"sg.ViewDistanceQuality 2")
        ExecuteConsoleCommand(gameInstance,"sg.AntiAliasingQuality 2")
        ExecuteConsoleCommand(gameInstance,"sg.ShadowQuality 2")
        ExecuteConsoleCommand(gameInstance,"sg.PostProcessQuality 2")
        ExecuteConsoleCommand(gameInstance,"sg.TextureQuality 2")
        ExecuteConsoleCommand(gameInstance,"sg.EffectsQuality 2")
        ExecuteConsoleCommand(gameInstance,"sg.FoliageQuality 2")
    end
end

function t:AdjustRenderParamByGPU()
    local gpuFamily = UE.UBoomSDKBPLibrary.GetGPUFamily()
    local rank = android_gpu_score[gpuFamily] 
    if not rank then 
        print("GPUFamily not config",gpuFamily)
        return
    end
   
    print("GPUFamilyInfo",gpuFamily,rank)
    if rank == RankEnum.Low0 then 
        self:SetParamLowest()
        self.isLowest = true 
    elseif rank == RankEnum.Low1 then 
        self:SetParamLow()
    elseif rank == RankEnum.Mid then 
        self:SetParamMid()
    else
        self:SetParamHigh()
    end
end

local Platform = require "LuaLib.Utility.Platform"
function t:ShowCPUInfo()
    local cpu_info = Platform.GetCPUInfo()
    print("CPU",cpu_info)
end

function t:DoEnterLobby()
    if self.isLowest then 
        print("GPU EnterLobby")
        local gameInstance = gameInstance
        local ExecuteConsoleCommand = UE.UKismetSystemLibrary.ExecuteConsoleCommand
        ExecuteConsoleCommand(gameInstance,"ShowFlag.Particles 0")
        --ExecuteConsoleCommand(gameInstance,"ShowFlag.Translucency 1")

        ExecuteConsoleCommand(gameInstance,"r.MobileContentScaleFactor 0.7")
        ExecuteConsoleCommand(gameInstance,"r.ScreenPercentage 100")
    end
end

function t:DoEnterFight()
    if self.isLowest then 
        print("GPU EnterFight")
        local gameInstance = gameInstance
        local ExecuteConsoleCommand = UE.UKismetSystemLibrary.ExecuteConsoleCommand
        ExecuteConsoleCommand(gameInstance,"ShowFlag.Particles 1")
        --ExecuteConsoleCommand(gameInstance,"ShowFlag.Translucency 0")

        ExecuteConsoleCommand(gameInstance,"r.AllowOcclusionQueries 1")

        ExecuteConsoleCommand(gameInstance,"r.MobileContentScaleFactor 0.5")
        ExecuteConsoleCommand(gameInstance,"r.ScreenPercentage 80")
    end
end


function t:DoEnterLogin()
    self:ShowCPUInfo()
    self:AdjustRenderParamByGPU()
end

return t 