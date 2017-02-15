# Mbed在自己的stm32系列平台移植适配

适配平台:
cpu:**STM32F103RCT6**
外设:  

|peripheral	|pin	|disciption|
| -------- | ----- | -------- |
| *LED1*     | PC_0  |          |
|*LED2*     | PC_6  |          |
| *UART5_TX* | PC_12 | no remap |
| *UART5_RX* | PD_2  | no remap |

引用资源:  
[mbed在线编译器][mbed在线编译器]  
[Mbed源码仓库][Mbed源码仓库]  
[Stm32f1官方hal库][Stm32f1官方hal库]  

## 一、前言
进入正篇前，需要介绍一些预备知识。
St的软件开发库有两套：标准库和hal库，通常早期的开发都是使用的标准库，不过现在标准库已经停止维护了，而且新出的芯片都没有适配标准库，只有hal库。而mbed底层正是使用的hal库。
在此处我们还需要了解一点东西就是在st的标准库中，我们将芯片分为hd，md，xl等系列，而在hal库中并没有沿用这样的命名方式，而是使用xb、xe、xg等命名方式
    
	#if !defined (STM32F100xB) && !defined (STM32F100xE) && !defined (STM32F101x6) && \
    !defined (STM32F101xB) && !defined (STM32F101xE) && !defined (STM32F101xG) && !defined (STM32F102x6) && !defined (STM32F102xB) && !defined (STM32F103x6) && \
    !defined (STM32F103xB) && !defined (STM32F103xE) && !defined (STM32F103xG) && !defined (STM32F105xC) && !defined (STM32F107xC)
	/* #define STM32F100xB */   /*!< STM32F100C4, STM32F100R4, STM32F100C6, STM32F100R6, STM32F100C8, STM32F100R8, STM32F100V8, STM32F100CB, STM32F100RB and STM32F100VB */
    /* #define STM32F100xE */   /*!< STM32F100RC, STM32F100VC, STM32F100ZC, STM32F100RD, STM32F100VD, STM32F100ZD, STM32F100RE, STM32F100VE and STM32F100ZE */
    /* #define STM32F101x6 */   /*!< STM32F101C4, STM32F101R4, STM32F101T4, STM32F101C6, STM32F101R6 and STM32F101T6 Devices */
    /* #define STM32F101xB */   /*!< STM32F101C8, STM32F101R8, STM32F101T8, STM32F101V8, STM32F101CB, STM32F101RB, STM32F101TB and STM32F101VB */
    /* #define STM32F101xE */   /*!< STM32F101RC, STM32F101VC, STM32F101ZC, STM32F101RD, STM32F101VD, STM32F101ZD, STM32F101RE, STM32F101VE and STM32F101ZE */ 
    /* #define STM32F101xG */   /*!< STM32F101RF, STM32F101VF, STM32F101ZF, STM32F101RG, STM32F101VG and STM32F101ZG */
    /* #define STM32F102x6 */   /*!< STM32F102C4, STM32F102R4, STM32F102C6 and STM32F102R6 */
    /* #define STM32F102xB */   /*!< STM32F102C8, STM32F102R8, STM32F102CB and STM32F102RB */
    /* #define STM32F103x6 */   /*!< STM32F103C4, STM32F103R4, STM32F103T4, STM32F103C6, STM32F103R6 and STM32F103T6 */
	/* #define STM32F103xB */   /*!< STM32F103C8, STM32F103R8, STM32F103T8, STM32F103V8, STM32F103CB, STM32F103RB, STM32F103TB and STM32F103VB */
    /* #define STM32F103xE */   /*!< STM32F103RC, STM32F103VC, STM32F103ZC, STM32F103RD, STM32F103VD, STM32F103ZD, STM32F103RE, STM32F103VE and STM32F103ZE */
    /* #define STM32F103xG */   /*!< STM32F103RF, STM32F103VF, STM32F103ZF, STM32F103RG, STM32F103VG and STM32F103ZG */
    /* #define STM32F105xC */   /*!< STM32F105R8, STM32F105V8, STM32F105RB, STM32F105VB, STM32F105RC and STM32F105VC */
    /* #define STM32F107xC */   /*!< STM32F107RB, STM32F107VB, STM32F107RC and STM32F107VC */  
    #endif
	
那么相关的头文件就是

    #if defined(STM32F100xB)
      #include "stm32f100xb.h"
    #elif defined(STM32F100xE)
      #include "stm32f100xe.h"
    #elif defined(STM32F101x6)
       #include "stm32f101x6.h"
    #elif defined(STM32F101xB)
       #include "stm32f101xb.h"
    #elif defined(STM32F101xE)
      #include "stm32f101xe.h"
    #elif defined(STM32F101xG)
      #include "stm32f101xg.h"
    #elif defined(STM32F102x6)
      #include "stm32f102x6.h"
    #elif defined(STM32F102xB)
      #include "stm32f102xb.h"
    #elif defined(STM32F103x6)
      #include "stm32f103x6.h"
    #elif defined(STM32F103xB)
     #include "stm32f103xb.h"
    #elif defined(STM32F103xE)
      #include "stm32f103xe.h"
    #elif defined(STM32F103xG)
      #include "stm32f103xg.h"
    #elif defined(STM32F105xC)
      #include "stm32f105xc.h"
    #elif defined(STM32F107xC)
      #include "stm32f107xc.h"
    #else
     #error "Please select first the target STM32F1xx device used in your application (in stm32f1xx.h file)"
    #endif
	
相关的启动文件就是

	startup_stm32f100xb.S
	startup_stm32f100xe.S
	startup_stm32f101x6.S
	startup_stm32f101xb.S
	startup_stm32f101xe.S
	startup_stm32f102x6.S
	startup_stm32f102xb.S
	startup_stm32f103x6.S
	startup_stm32f103xb.S
	startup_stm32f103xe.S
	startup_stm32f103xg.S
	startup_stm32f105xc.S
	startup_stm32f107xc.S
	
相关的分散文件就是

    stm32f100xb.sct
    stm32f100xe.sct
    stm32f101x6.sct
    stm32f101xb.sct
    stm32f101xe.sct
    stm32f102x6.sct
    stm32f102xb.sct
    stm32f103x6.sct
	stm32f103xb.sct
	stm32f103xe.sct
	stm32f103xg.sct
	stm32f105xc.sct
	stm32f107xc.sct
	
由于STM32f103RB属于xb系列，而stm32f103RC属于xe系列，所以我们需要使用xe系列的文件。上面提到的有些文件有现成的可以使用，有些则需要基于stm32f103xb系列文件做适配得到。

## 二、构建源码工程
### 1获取NUCLEO_F103RB的模版
既然是根据nucleo_F103RB来适配，当然需要有一个nucleo_F103RB的模版才行，当然没有也是可以的，我们可以手动通过MDK创建一个全新的工程。但是配置一些编译选项可能比较麻烦，所以我们还是通过nucleo_F103RB的模版来修改吧。
打开[mbed的官网][mbed在线编译器]，进入developer，然后点击编辑器compiler，当然如果没有帐号的先注册一个帐号吧。  
![][1]  
然后选择一个开发板，此处我们选择nucleo-f103RB
![][2]  
确认选择后我们就可以新建工程了。  
![][3]  
点击OK后工程建立完成，不过mbed的底层文件都被掩藏起来了，是看不到源码的。
然后我们将工程导出，此处我们到处为mdk v5  
![][4]  
![][5]  
至此，我们就拥有了一个nucleo-f103rb的模版，只不过打开这个工程的文件夹后我们可以看到mbed里面全都是.o文件，并不是我们希望的源码，因为我们要适配必须要源码才行，.o文件是没有办法修改的。
### 2建立nucleo-f103rb的源码工程
我们知道，mbed os是开源项目，那么之前看到的.o文件都是通过这些源码编译后生成的，我们只要后去了mbed的源码，然后添加到工程中，然后稍作配置即可编译成功了。
从mbed的github下载mbed的源码:
[mbed源码][Mbed源码仓库]
下载成功后会看到这样的一些文件  
![][6]  
将nucleo-f103rb工程目录中mbed里面的所有文件全部删除，然后将mbed源码中的文件全部拷贝，一些文档类的文件可以删除。
当然为了是工程结构更加简洁，我们新建一个user和project文件夹，然后将project文件移入project中，将main和mbed_config.h文件移入user中。
打开工程，将之前的文件输出掉，然后添加新的资源文件到工程中，注意观察原本的工程包含了那些文件夹，比如drivers、hal、platform等、对应着添加，原本没有添加的就不需要加进去了，比如原本event没有添加到工程中，那么我们添加源码时event就可以不用添加了。但是注意一定要添加完整，不然可能会出现编译错误的情况。  
![][7]  
然后修改头文件包含路径，将存在头文件的路径全部添加即可。  
![][8]  
设置sct文件，  
![][9]  
将sct文件定位到mbed实际存在的路径上。
在mbed\targets\TARGET_STM\TARGET_STM32F1\TARGET_NUCLEO_F103RB\device\TOOLCHAIN_ARM_STD中。然后就可以尝试着编译了，如果有问题照着问题的提示慢慢修改，直到没有error为止，如果文件添加完整，路径设置正确，sct设置正确应该就没有错误的。然后就是开始适配了。
## 三、适配开发板
### 1适配芯片
首先将芯片修改为stm32f103RC  
![][10]  
然后从[st官网的hal库][Stm32f1官方hal库]中拷贝其他芯片的头文件和启动文件过来，
同时mbed工程中的sct文件只有stm32f103xb.sct，我们复制一分然后重命名为stm32f103xe.sct。
修改stm32f1xx.h文件，注释掉#define STM32F103xB，取消注释#define STM32F103xE。

	#if !defined (STM32F100xB) && !defined (STM32F100xE) && !defined (STM32F101x6) && \
		!defined (STM32F101xB) && !defined (STM32F101xE) && !defined (STM32F101xG) && !defined 	  (STM32F102x6) && !defined (STM32F102xB) && !defined (STM32F103x6) && \
		!defined (STM32F103xB) && !defined (STM32F103xE) && !defined (STM32F103xG) && !defined (STM32F105xC) && !defined (STM32F107xC)
	  /* #define STM32F100xB */   /*!< STM32F100C4, STM32F100R4, STM32F100C6, STM32F100R6, STM32F100C8, STM32F100R8, STM32F100V8, STM32F100CB, STM32F100RB and STM32F100VB */
	  /* #define STM32F100xE */   /*!< STM32F100RC, STM32F100VC, STM32F100ZC, STM32F100RD, STM32F100VD, STM32F100ZD, STM32F100RE, STM32F100VE and STM32F100ZE */
	  /* #define STM32F101x6 */   /*!< STM32F101C4, STM32F101R4, STM32F101T4, STM32F101C6, STM32F101R6 and STM32F101T6 Devices */
	  /* #define STM32F101xB */   /*!< STM32F101C8, STM32F101R8, STM32F101T8, STM32F101V8, STM32F101CB, STM32F101RB, STM32F101TB and STM32F101VB */
	  /* #define STM32F101xE */   /*!< STM32F101RC, STM32F101VC, STM32F101ZC, STM32F101RD, STM32F101VD, STM32F101ZD, STM32F101RE, STM32F101VE and STM32F101ZE */ 
	  /* #define STM32F101xG */   /*!< STM32F101RF, STM32F101VF, STM32F101ZF, STM32F101RG, STM32F101VG and STM32F101ZG */
	  /* #define STM32F102x6 */   /*!< STM32F102C4, STM32F102R4, STM32F102C6 and STM32F102R6 */
	  /* #define STM32F102xB */   /*!< STM32F102C8, STM32F102R8, STM32F102CB and STM32F102RB */
	  /* #define STM32F103x6 */   /*!< STM32F103C4, STM32F103R4, STM32F103T4, STM32F103C6, STM32F103R6 and STM32F103T6 */
	/* #define STM32F103xB */   /*!< STM32F103C8, STM32F103R8, STM32F103T8, STM32F103V8, STM32F103CB, STM32F103RB, STM32F103TB and STM32F103VB */
	   #define STM32F103xE    /*!< STM32F103RC, STM32F103VC, STM32F103ZC, STM32F103RD, STM32F103VD, STM32F103ZD, STM32F103RE, STM32F103VE and STM32F103ZE */
	  /* #define STM32F103xG */   /*!< STM32F103RF, STM32F103VF, STM32F103ZF, STM32F103RG, STM32F103VG and STM32F103ZG */
	  /* #define STM32F105xC */   /*!< STM32F105R8, STM32F105V8, STM32F105RB, STM32F105VB, STM32F105RC and STM32F105VC */
	  /* #define STM32F107xC*/    /*!< STM32F107RB, STM32F107VB, STM32F107RC and STM32F107VC */  
	#endif
好了，芯片的匹配工作完成，注意由于原本工程中的启动文件是用的startup_stm32f103xb.S，需要修改成startup_stm32f103xe.S  
![][11]  
同时sct文件路径也要指定为stm32f103xe.sct

### 2适配晶振频率(如果不需要修改的可以跳过该步骤)
因为默认的开发板使用的是8MHz晶振，而我用的是12MHz，所以需要做晶振频率的修改。
修改文件system_stm32f1xx.c(注意mbed中的该文件内部集成了时钟初始化，而官方自带的hal中该文件没有进行时钟的初始化)
我们先来对比一下system_stm32f1xx.c文件的SystemInit函数
这是mbed的自带的

		void SystemInit (void)
		{
		  /* Reset the RCC clock configuration to the default reset state(for debug purpose) */
		  /* Set HSION bit */
		  RCC->CR |= (uint32_t)0x00000001;

		  /* Reset SW, HPRE, PPRE1, PPRE2, ADCPRE and MCO bits */
		#if !defined(STM32F105xC) && !defined(STM32F107xC)
		  RCC->CFGR &= (uint32_t)0xF8FF0000;
		#else
		  RCC->CFGR &= (uint32_t)0xF0FF0000;
		#endif /* STM32F105xC */   

		  /* Reset HSEON, CSSON and PLLON bits */
		  RCC->CR &= (uint32_t)0xFEF6FFFF;

		  /* Reset HSEBYP bit */
		  RCC->CR &= (uint32_t)0xFFFBFFFF;

		  /* Reset PLLSRC, PLLXTPRE, PLLMUL and USBPRE/OTGFSPRE bits */
		  RCC->CFGR &= (uint32_t)0xFF80FFFF;

		#if defined(STM32F105xC) || defined(STM32F107xC)
		  /* Reset PLL2ON and PLL3ON bits */
		  RCC->CR &= (uint32_t)0xEBFFFFFF;

		  /* Disable all interrupts and clear pending bits  */
		  RCC->CIR = 0x00FF0000;

		  /* Reset CFGR2 register */
		  RCC->CFGR2 = 0x00000000;
		#elif defined(STM32F100xB) || defined(STM32F100xE)
		  /* Disable all interrupts and clear pending bits  */
		  RCC->CIR = 0x009F0000;

		  /* Reset CFGR2 register */
		  RCC->CFGR2 = 0x00000000;      
		#else
		  /* Disable all interrupts and clear pending bits  */
		  RCC->CIR = 0x009F0000;
		#endif /* STM32F105xC */

		#if defined(STM32F100xE) || defined(STM32F101xE) || defined(STM32F101xG) || defined(STM32F103xE) || defined(STM32F103xG)
		  #ifdef DATA_IN_ExtSRAM
			SystemInit_ExtMemCtl(); 
		  #endif /* DATA_IN_ExtSRAM */
		#endif 

		#ifdef VECT_TAB_SRAM
		  SCB->VTOR = SRAM_BASE | VECT_TAB_OFFSET; /* Vector Table Relocation in Internal SRAM. */
		#else
		  SCB->VTOR = FLASH_BASE | VECT_TAB_OFFSET; /* Vector Table Relocation in Internal FLASH. */
		#endif

		  /* Configure the Cube driver */
		  SystemCoreClock = 8000000; // At this stage the HSI is used as system clock
		  HAL_Init();

		  /* Configure the System clock source, PLL Multiplier and Divider factors,
			 AHB/APBx prescalers and Flash settings */
		  SetSysClock();

		  /* Reset the timer to avoid issues after the RAM initialization */
		  TIM_MST_RESET_ON;
		  TIM_MST_RESET_OFF;
		}
我们可以从中可以看到调用了SetSysClock()函数，这个函数就是进行时钟设置的。
相反的如果我们从st自带的hal库中打开一个Example，可以看到st的hal库中的时钟设置部分都是放在main函数的开头的。
其实道理是一样的，因为systemInit执行完了后接着就会执行main函数了，所以时钟初始化放在systeminit的末位和放在main的开头是等效的。

好了，开始适配晶振。由于我使用的是12MHz的晶振，通过12MHz*6=72MHz来产生72MHz的主频。因为时钟初始化实是在SetSysClock中。
跟踪
SetSysClock-->SetSysClock_PLL_HSE。我们可以知道需要修改SetSysClock_PLL_HSE函数，

		RCC_OscInitStruct.HSEPredivValue      = RCC_HSE_PREDIV_DIV1;
		RCC_OscInitStruct.PLL.PLLState        = RCC_PLL_ON;
		RCC_OscInitStruct.PLL.PLLSource       = RCC_PLLSOURCE_HSE;
		RCC_OscInitStruct.PLL.PLLMUL          = RCC_PLL_MUL9; // 72 MHz (8 MHz * 9)
将RCC_PLL_MUL9改为RCC_PLL_MUL6，因为我们将使用12MHz*6=72MHz的倍频方式

然后在整个工程中全局搜索HSE_VALUE定义
可以得到在stm32f1xx_hal_conf.h和system_stm32f1xx.c中分别有定义，比如我用的12MHz，我就修改成12000000
理论上只需要修改stm32f1xx_hal_conf.h中的即可，但是为了安全还是全部改了吧。

### 3适配分散文件sct
mbed对堆栈的定义做了自己的定义这个跟st自带的堆栈分配并不一样，所以需要做修改，这样就直接导致了sct的空间分布需要修改。打开mbed自带的stm32f103xb.sct文件。

		LR_IROM1 0x08000000 0x20000  {    ; load region size_region (128K)

		  ER_IROM1 0x08000000 0x20000  {  ; load address = execution address
		   *.o (RESET, +First)
		   *(InRoot$$Sections)
		   .ANY (+RO)
		  }

		  ; 59 vectors (16 core + 43 peripheral) * 4 bytes = 236 bytes to reserve (0xEC)
		  RW_IRAM1 (0x20000000+0xEC) (0x5000-0xEC)  {  ; RW data
		   .ANY (+RW +ZI)
		  }

		}
我们可以从中看到在ram的分配上预留了大小为0xEC的空间，而这个空间的大小是根据中断向量个数来决定的，可以猜测这个预留空间可能会将向量表重载到这个地方。我们将这个文件适配成stm32f103RC使用的。
因为stm32f103RC的flash=0x40000，ram=0xC000，中断个数可以查看启动文件。

	__Vectors       DCD     __initial_sp               ; Top of Stack
                DCD     Reset_Handler              ; Reset Handler
                DCD     NMI_Handler                ; NMI Handler
                DCD     HardFault_Handler          ; Hard Fault Handler
                DCD     MemManage_Handler          ; MPU Fault Handler
                DCD     BusFault_Handler           ; Bus Fault Handler
                DCD     UsageFault_Handler         ; Usage Fault Handler
                DCD     0                          ; Reserved
                DCD     0                          ; Reserved
                DCD     0                          ; Reserved
                DCD     0                          ; Reserved
                DCD     SVC_Handler                ; SVCall Handler
                DCD     DebugMon_Handler           ; Debug Monitor Handler
                DCD     0                          ; Reserved
                DCD     PendSV_Handler             ; PendSV Handler
                DCD     SysTick_Handler            ; SysTick Handler

                ; External Interrupts
                DCD     WWDG_IRQHandler            ; Window Watchdog
                DCD     PVD_IRQHandler             ; PVD through EXTI Line detect
                DCD     TAMPER_IRQHandler          ; Tamper
                DCD     RTC_IRQHandler             ; RTC
                DCD     FLASH_IRQHandler           ; Flash
                DCD     RCC_IRQHandler             ; RCC
                DCD     EXTI0_IRQHandler           ; EXTI Line 0
                DCD     EXTI1_IRQHandler           ; EXTI Line 1
                DCD     EXTI2_IRQHandler           ; EXTI Line 2
                DCD     EXTI3_IRQHandler           ; EXTI Line 3
                DCD     EXTI4_IRQHandler           ; EXTI Line 4
                DCD     DMA1_Channel1_IRQHandler   ; DMA1 Channel 1
                DCD     DMA1_Channel2_IRQHandler   ; DMA1 Channel 2
                DCD     DMA1_Channel3_IRQHandler   ; DMA1 Channel 3
                DCD     DMA1_Channel4_IRQHandler   ; DMA1 Channel 4
                DCD     DMA1_Channel5_IRQHandler   ; DMA1 Channel 5
                DCD     DMA1_Channel6_IRQHandler   ; DMA1 Channel 6
                DCD     DMA1_Channel7_IRQHandler   ; DMA1 Channel 7
                DCD     ADC1_2_IRQHandler          ; ADC1 & ADC2
                DCD     USB_HP_CAN1_TX_IRQHandler  ; USB High Priority or CAN1 TX
                DCD     USB_LP_CAN1_RX0_IRQHandler ; USB Low  Priority or CAN1 RX0
                DCD     CAN1_RX1_IRQHandler        ; CAN1 RX1
                DCD     CAN1_SCE_IRQHandler        ; CAN1 SCE
                DCD     EXTI9_5_IRQHandler         ; EXTI Line 9..5
                DCD     TIM1_BRK_IRQHandler        ; TIM1 Break
                DCD     TIM1_UP_IRQHandler         ; TIM1 Update
                DCD     TIM1_TRG_COM_IRQHandler    ; TIM1 Trigger and Commutation
                DCD     TIM1_CC_IRQHandler         ; TIM1 Capture Compare
                DCD     TIM2_IRQHandler            ; TIM2
                DCD     TIM3_IRQHandler            ; TIM3
                DCD     TIM4_IRQHandler            ; TIM4
                DCD     I2C1_EV_IRQHandler         ; I2C1 Event
                DCD     I2C1_ER_IRQHandler         ; I2C1 Error
                DCD     I2C2_EV_IRQHandler         ; I2C2 Event
                DCD     I2C2_ER_IRQHandler         ; I2C2 Error
                DCD     SPI1_IRQHandler            ; SPI1
                DCD     SPI2_IRQHandler            ; SPI2
                DCD     USART1_IRQHandler          ; USART1
                DCD     USART2_IRQHandler          ; USART2
                DCD     USART3_IRQHandler          ; USART3
                DCD     EXTI15_10_IRQHandler       ; EXTI Line 15..10
                DCD     RTC_Alarm_IRQHandler        ; RTC Alarm through EXTI Line
                DCD     USBWakeUp_IRQHandler       ; USB Wakeup from suspend
                DCD     TIM8_BRK_IRQHandler        ; TIM8 Break
                DCD     TIM8_UP_IRQHandler         ; TIM8 Update
                DCD     TIM8_TRG_COM_IRQHandler    ; TIM8 Trigger and Commutation
                DCD     TIM8_CC_IRQHandler         ; TIM8 Capture Compare
                DCD     ADC3_IRQHandler            ; ADC3
                DCD     FSMC_IRQHandler            ; FSMC
                DCD     SDIO_IRQHandler            ; SDIO
                DCD     TIM5_IRQHandler            ; TIM5
                DCD     SPI3_IRQHandler            ; SPI3
                DCD     UART4_IRQHandler           ; UART4
                DCD     UART5_IRQHandler           ; UART5
                DCD     TIM6_IRQHandler            ; TIM6
                DCD     TIM7_IRQHandler            ; TIM7
                DCD     DMA2_Channel1_IRQHandler   ; DMA2 Channel1
                DCD     DMA2_Channel2_IRQHandler   ; DMA2 Channel2
                DCD     DMA2_Channel3_IRQHandler   ; DMA2 Channel3
                DCD     DMA2_Channel4_5_IRQHandler ; DMA2 Channel4 & Channel5
    __Vectors_End
数了一下总共是16+60=76个，所以sct可以这样写：

	LR_IROM1 0x08000000 0x40000  {    ; load region size_region (128K)

	  ER_IROM1 0x08000000 0x40000  {  ; load address = execution address
	   *.o (RESET, +First)
	   *(InRoot$$Sections)
	   .ANY (+RO)
	  }

	  ; 76 vectors (16 core + 60 peripheral) * 4 bytes = 304 bytes to reserve (0x130)
	  RW_IRAM1 (0x20000000+0x130) (0xC000-0x130)  {  ; RW data
	   .ANY (+RW +ZI)
	  }

	}

### 4适配启动文件
因为需要重新定义堆栈，所以堆栈地址需要修改，同时默认的开发板使用的是stm32f103RB，而我用的是stm32f103RC，支持的中断和外设比RB要多，所以需要加上去，此处可以使用st官方的hal库中的RC启动文件，然后修改堆栈地址。
删除掉自带的堆栈设置，添加mbed需要的堆栈地址  
![][12]  
然后删除掉自带文件的堆栈初始化操作  
![][13]  
### 5适配pinname，peripheralname和peripheralpin
关于这三个东西，如果我们仔细研究一下他们的源码后，我们就会发现一个很有意思的东西
PeripheralPins
PeripheralNames
PinNames
这三个文件可以剥离出三个东西，peripheral、pin和name
Name好理解，主体是pin和peripheral
Pin的注册名称就是pinnames

	LED1        = PC_0,
	LED2        = PC_6,
	LED3        = PC_0,
	LED4        = PC_6,
	USER_BUTTON = PC_13,
	SERIAL_TX   = PA_9,
	SERIAL_RX   = PA_10,
	USBTX       = PA_2,
	USBRX       = PA_3,
peripheral的注册名就是peripheralnames

	typedef enum {
		UART_1 = (int)USART1_BASE,
		UART_2 = (int)USART2_BASE,
		UART_3 = (int)USART3_BASE,
		UART_4 = (int)UART4_BASE,
		UART_5 = (int)UART5_BASE,
	} UARTName;

将peripheral和pin组合在一起同时添加一些特征功能就是peripheralpin

	const PinMap PinMap_UART_TX[] = {
		{PA_2,  UART_2, STM_PIN_DATA(STM_MODE_AF_PP, GPIO_PULLUP, 0)},
		{PA_9,  UART_1, STM_PIN_DATA(STM_MODE_AF_PP, GPIO_PULLUP, 0)},
		{PB_6,  UART_1, STM_PIN_DATA(STM_MODE_AF_PP, GPIO_PULLUP, 3)}, // GPIO_Remap_USART1
		{PB_10, UART_3, STM_PIN_DATA(STM_MODE_AF_PP, GPIO_PULLUP, 0)},
		{PC_10, UART_3, STM_PIN_DATA(STM_MODE_AF_PP, GPIO_PULLUP, 5)}, // GPIO_PartialRemap_USART3
		{PC_12, UART_5, STM_PIN_DATA(STM_MODE_AF_PP, GPIO_PULLUP, 0)},
		{NC,    NC,     0}
	};
peripheralpin就是跟上层打交道的。打交道的api集中在pinmap中  
![][14]  
现在开始适配这三项
比如我的外设是这样的
LED1-------------------PC_0
LED2-------------------PC_6
UART5_TX------------PC_12
UART5_RX------------PD_2
添加pinname

	LED1        = PC_0,
    LED2        = PC_6,
	.....
	SERIAL_TX   = PA_9,
    SERIAL_RX   = PA_10,
添加peripheralname

	UART_4 = (int)UART4_BASE,
	UART_5 = (int)UART5_BASE,
添加peripheralpin
在PinMap_UART_TX中添加

	{PC_12, UART_5, STM_PIN_DATA(STM_MODE_AF_PP, GPIO_PULLUP, 0)},
该句一定要放在结束符

	{NC,    NC,     0}
之前
同理在PinMap_UART_RX中添加

	{PD_2,  UART_5, STM_PIN_DATA(STM_MODE_INPUT, GPIO_PULLUP, 0)},
关于STM_PIN_DATA()，这其实是一个宏定义，最后一个参数是一个复用的索引表，这个索引表在pinmap文件中有所体现。

	switch (afnum) {
			case 1: // Remap SPI1
				__HAL_AFIO_REMAP_SPI1_ENABLE();
				break;
			case 2: // Remap I2C1
				__HAL_AFIO_REMAP_I2C1_ENABLE();
				break;
			case 3: // Remap USART1
				__HAL_AFIO_REMAP_USART1_ENABLE();
				break;
			case 4: // Remap USART2
				__HAL_AFIO_REMAP_USART2_ENABLE();
				break;
			case 5: // Partial Remap USART3
				__HAL_AFIO_REMAP_USART3_PARTIAL();
				break;
			case 6: // Partial Remap TIM1
				__HAL_AFIO_REMAP_TIM1_PARTIAL();
				break;
			case 7: // Partial Remap TIM3
				__HAL_AFIO_REMAP_TIM3_PARTIAL();
				break;
			case 8: // Full Remap TIM2
				__HAL_AFIO_REMAP_TIM2_ENABLE();
				break;
			case 9: // Full Remap TIM3
				__HAL_AFIO_REMAP_TIM3_ENABLE();
				break;
			case 10: // CAN_RX mapped to PB8, CAN_TX mapped to PB9
				__HAL_AFIO_REMAP_CAN1_2();
				break;
			default:
				break;
	}
具体对应表格如下：

|num|discription|function|
|----|-----|-----|
|1|Remap SPI1|__HAL_AFIO_REMAP_SPI1_ENABLE|
|2|Remap I2C1|__HAL_AFIO_REMAP_I2C1_ENABLE|
|3|Remap USART1|__HAL_AFIO_REMAP_USART1_ENABLE|
|4|Remap USART2|__HAL_AFIO_REMAP_USART2_ENABLE|
|5|Partial Remap USART3|__HAL_AFIO_REMAP_USART3_PARTIAL|
|6|Partial Remap TIM1|__HAL_AFIO_REMAP_TIM1_PARTIAL|
|7|Partial Remap TIM3|__HAL_AFIO_REMAP_TIM3_PARTIAL|
|8|Full Remap TIM2|__HAL_AFIO_REMAP_TIM2_ENABLE|
|9|Full Remap TIM3|__HAL_AFIO_REMAP_TIM3_ENABLE|
|10|CAN_RX mapped to PB8/CAN_TX mapped to PB9|__HAL_AFIO_REMAP_CAN1_2|
### 6适配串口初始化
#### a修改标准输入输出端口：
修改PeripheralNames

	#define STDIO_UART_TX  PC_12
	#define STDIO_UART_RX  PD_2
	#define STDIO_UART     UART_5
这是标准输入输出终端串口配置
#### b修改波特率
Mbedconfig.h

    #define MBED_CONF_PLATFORM_STDIO_BAUD_RATE          9600
    #define MBED_CONF_PLATFORM_DEFAULT_SERIAL_BAUD_RATE  9600
第一个是标准输入输出串口的默认波特率设置
第二个是普通串口的默认波特率设置

#### c添加初始化
串口的初始化程序在serial_api.c文件中
void serial_init(serial_t *obj, PinName tx, PinName rx)
由于自带的只有USART_1、USART_2和USART_3，我们现在要适配UART_4和UART_5，那么凡是有USART_1、USART_2和USART_3的地方我们都要参照这适配出UART_4和UART_5，全局搜索USART_3，找出需要增加UART_4和UART_5的地方，

serial_init函数中：

	if (obj_s->uart == UART_1) {
        __HAL_RCC_USART1_FORCE_RESET();
        __HAL_RCC_USART1_RELEASE_RESET();
        __HAL_RCC_USART1_CLK_ENABLE();
        obj_s->index = 0;
    }
    if (obj_s->uart == UART_2) {
        __HAL_RCC_USART2_FORCE_RESET();
        __HAL_RCC_USART2_RELEASE_RESET();
        __HAL_RCC_USART2_CLK_ENABLE();
        obj_s->index = 1;
    }
    if (obj_s->uart == UART_3) {
        __HAL_RCC_USART3_FORCE_RESET();
        __HAL_RCC_USART3_RELEASE_RESET();
        __HAL_RCC_USART3_CLK_ENABLE();
        obj_s->index = 2;
    }
	在后面添加
	
	if (obj_s->uart == UART_4) {
        __HAL_RCC_UART4_FORCE_RESET();
        __HAL_RCC_UART4_RELEASE_RESET();
        __HAL_RCC_UART4_CLK_ENABLE();
        obj_s->index = 3;
    }
		if (obj_s->uart == UART_5) {
        __HAL_RCC_UART5_FORCE_RESET();
        __HAL_RCC_UART5_RELEASE_RESET();
        __HAL_RCC_UART5_CLK_ENABLE();
        obj_s->index = 4;
    }
同时我么注意到obj_s->index也在增加，查找一下发现obj_s->index跟串口个数有关所以UART_NUM修改成 5
	
	#define UART_NUM (5)

	static uint32_t serial_irq_ids[UART_NUM] = {0};
	static UART_HandleTypeDef uart_handlers[UART_NUM];

同时还有两处的USART_3要适配成UART_5
serial_free函数中：

	if (obj_s->uart == UART_1) {
		__USART1_FORCE_RESET();
		__USART1_RELEASE_RESET();
		__USART1_CLK_DISABLE();
	}
	if (obj_s->uart == UART_2) {
		__USART2_FORCE_RESET();
		__USART2_RELEASE_RESET();
		__USART2_CLK_DISABLE();
	}
	if (obj_s->uart == UART_3) {
		__USART3_FORCE_RESET();
		__USART3_RELEASE_RESET();
		__USART3_CLK_DISABLE();
	}
在后面添加

	if (obj_s->uart == UART_4) {
        __UART4_FORCE_RESET();
        __UART4_RELEASE_RESET();
        __UART4_CLK_DISABLE();
    }
		if (obj_s->uart == UART_5) {
        __UART5_FORCE_RESET();
        __UART5_RELEASE_RESET();
        __UART5_CLK_DISABLE();
    }
	
在serial_irq_set函数中

	if (obj_s->uart == UART_1) {
        irq_n = USART1_IRQn;
        vector = (uint32_t)&uart1_irq;
    }

    if (obj_s->uart == UART_2) {
        irq_n = USART2_IRQn;
        vector = (uint32_t)&uart2_irq;
    }

    if (obj_s->uart == UART_3) {
        irq_n = USART3_IRQn;
        vector = (uint32_t)&uart3_irq;
    }
在后面添加
	
	if (obj_s->uart == UART_4) {
        irq_n = UART4_IRQn;
        vector = (uint32_t)&uart4_irq;
    }
		
	if (obj_s->uart == UART_5) {
        irq_n = UART5_IRQn;
        vector = (uint32_t)&uart5_irq;
    }
然后发现uart4_irq和uart5_irq没有定义，我们搜索一下uart3_irq，并参照着uart3_irq定义uart4_irq和uart5_irq

	static void uart4_irq(void)
	{
		uart_irq(3);
	}

	static void uart5_irq(void)
	{
		uart_irq(4);
	}
同时修改uart_irq，添加参数3和参数4的部分

	if (__HAL_UART_GET_FLAG(huart, UART_FLAG_TC) != RESET) {
		if (__HAL_UART_GET_IT_SOURCE(huart, UART_IT_TC) != RESET) {
			irq_handler(serial_irq_ids[id], TxIrq);
			__HAL_UART_CLEAR_FLAG(huart, UART_FLAG_TC);
		}
	}
	if (__HAL_UART_GET_FLAG(huart, UART_FLAG_RXNE) != RESET) {
		if (__HAL_UART_GET_IT_SOURCE(huart, UART_IT_RXNE) != RESET) {
			irq_handler(serial_irq_ids[id], RxIrq);
			__HAL_UART_CLEAR_FLAG(huart, UART_FLAG_RXNE);
		}
	}
	if (__HAL_UART_GET_FLAG(huart, UART_FLAG_ORE) != RESET) {
		if (__HAL_UART_GET_IT_SOURCE(huart, UART_IT_ERR) != RESET) {
			volatile uint32_t tmpval = huart->Instance->DR; // Clear ORE flag
		}
	}
发现没什么要修改的。

修改完这些之后，编译应该就没有问题了，下载到开发板中也能工作正常了。  
![][15]  
### 7关于编译选项的研究
为什么要研究编译选项？细心的同学可能会注意到我前面创建工程的一个细节，我的工程并不是自己使用MDK手动创建的，而是通过在线的编译器导出的。然后我有将工程中的所有文件全部更换成了mbed源码库中的文件和st hal官方库中的文件。既然文件我全部都替换了，那么我为什么不自己用MDK手动建立一个新工程呢？原因就在于编译选项上。手动新建的工程使用了一些默认的编译选项，而我们导出的mbed工程使用了一些自定义的编译选项，这些选项太多了，设置起来比较麻烦，所以我为了方便，就直接引用了导入的工程。
那么现在你是否能够想到另外的一些想法：我用MDK手动新建一个工程，然后参照这mbed导出工程的编译选项来调整这个工程，那么这样的工程是否可用呢？答案是完全没问题。所以，现在我们得到了两种创建工程的方法。
第一种：使用mbed在线编译器导出工程，然后替换所有的mbed文件。
第二种：使用MDK手动创建工程，然后添加mbed库文件，然后照着之前导出的mbed编译选项设置。
所以，现在我们就需要来研究一下mbed的编译选项，因为这不仅关系到工程创建，同样关系到工程移植。  
![][16]  
为了更方便研究，我们直接将其复制到文本编辑器中:

	-DDEVICE_RTC=1 -DDEVICE_SLEEP=1 -DTOOLCHAIN_object -DTOOLCHAIN_ARM_STD -D__ASSERT_MSG -DTARGET_STM32F1 --no_rtti -DTARGET_STM32F103RB -DMBED_BUILD_TIMESTAMP=1484039781.98 -Otime -DDEVICE_PORTINOUT=1 -D__CORTEX_M3 -DTARGET_FF_ARDUINO -c -O3 -DDEVICE_CAN=1 -DDEVICE_PORTOUT=1 -DDEVICE_STDIO_MESSAGES=1 -DTARGET_RELEASE --split_sections -DARM_MATH_CM3 -DTARGET_LIKE_CORTEX_M3 -DDEVICE_ANALOGIN=1 -DTARGET_NUCLEO_F103RB -DDEVICE_PORTIN=1 -DTARGET_CORTEX_M --cpu=Cortex-M3 -DTARGET_FF_MORPHO -DDEVICE_I2C=1 --preinclude=mbed_config.h -DTARGET_STM -DTOOLCHAIN_ARM -DDEVICE_INTERRUPTIN=1 --no_depend_system_headers -DTARGET_UVISOR_UNSUPPORTED --md -DDEVICE_PWMOUT=1 -DDEVICE_SERIAL_ASYNCH=1 --gnu --apcs=interwork -DDEVICE_SPI=1 -D__MBED__=1 -DDEVICE_SPISLAVE=1 -DDEVICE_SERIAL=1 -DTARGET_M3 -DDEVICE_I2CSLAVE=1 -D__CMSIS_RTOS -D__MBED_CMSIS_RTOS_CM -DTARGET_LIKE_MBED

-D开头的都是预编译宏定义，等效于define中的定义  
![][17]  
这是所有的-D选项，我们可以将这些选项直接设置在Define选项栏中

	-DDEVICE_RTC=1 
	-DDEVICE_SLEEP=1 
	-DTOOLCHAIN_object (x)
	-DTOOLCHAIN_ARM_STD 
	-D__ASSERT_MSG (x)
	-DTARGET_STM32F1 
	-DTARGET_STM32F103RB 
	-DDEVICE_PORTINOUT=1 
	-D__CORTEX_M3 
	-DTARGET_FF_ARDUINO 
	-DDEVICE_CAN=1 
	-DDEVICE_PORTOUT=1 
	-DDEVICE_STDIO_MESSAGES=1 
	-DTARGET_RELEASE 
	-DARM_MATH_CM3 
	-DTARGET_LIKE_CORTEX_M3 
	-DDEVICE_ANALOGIN=1 
	-DTARGET_NUCLEO_F103RB 
	-DDEVICE_PORTIN=1 
	-DTARGET_CORTEX_M 
	-DTARGET_FF_MORPHO 
	-DDEVICE_I2C=1 
	-DTARGET_STM -DTOOLCHAIN_ARM 
	-DDEVICE_INTERRUPTIN=1 
	-DTARGET_UVISOR_UNSUPPORTED 
	-DDEVICE_PWMOUT=1 
	-DDEVICE_SERIAL_ASYNCH=1 
	-DDEVICE_SPI=1 
	-D__MBED__=1 
	-DDEVICE_SPISLAVE=1 
	-DMBED_BUILD_TIMESTAMP=1484275342.19 
	-DDEVICE_SERIAL=1 
	-DTARGET_M3 
	-DDEVICE_I2CSLAVE=1 
	-D__CMSIS_RTOS 
	-D__MBED_CMSIS_RTOS_CM 
	-DTARGET_LIKE_MBED
这是11个非-D选项

	--no_rtti 
	-Otime (Optimize for Time)
	-c 
	-O3 (Optimization)
	--split_sections 
	--cpu=Cortex-M3 
	--preinclude=mbed_config.h 
	--no_depend_system_headers 
	--md 
	--gnu 
	--apcs=interwork 
这几个选项我们来看看什么意思，编译选项的含义我们需要查阅arm的官方编译手册  
![][18]  
-no_rtti

	Controls support for the RTTI features dynamic_cast and typeid in C++.
	Usage
	Use --no_rtti to disable source-level RTTI features such as dynamic_cast.
	 Note 
	You are permitted to use dynamic_cast without --rtti in cases where RTTI is not required, such as
	dynamic cast to an unambiguous base, and dynamic cast to (void *). If you try to use dynamic_cast
	without --rtti in cases where RTTI is required, the compiler generates an error.
这个选项是针对C++的语法支持的，需要详细了解自己百度谷歌。
-Otime

	Performs optimizations to reduce execution time at the expense of a possible increase in image size.
	Use this option if execution time is more critical than code size. If required, you can compile the time-
	critical parts of your code with -Otime, and the rest with -Ospace.
	Default
	If you do not specify -Otime, the compiler assumes -Ospace.
这个选项相当于MDK自带的设置选项Optimize for Time  
![][19]  
-c 
这个好理解，就是只编译，不链接，默认选项就是带有这个选项的。

-O3
优化等级，相当于MDK自带的Optimization选项  
![][20]  
--split_sections 
太专业的咋也说不清，看手册
--cpu=Cortex-M3
这个选项好懂，只要芯片选择了，这个选项会自动添加上的

--preinclude=mbed_config.h 
--preinclude选项用来自定头文件的路径，等效于MDK自带的include设置项  
![][21]  
-no_depend_system_headers 
--md 
--gnu 
--apcs=interwork 
这四个直接查阅手册吧。
介绍了上面的这些选项可能并不太懂什么意思，没关系，照着写就行了。

下面我们看看-D的一些选项，这些选项我们可以到源码中通过全局搜索看看在什么地方使用了这些选项，然后分析这些选项有什么用。
我们搜索一下  
![][22]  
注意此处look in选项和include sub-folders选项，因为我们mbed工程中的有些文件并没有包含到工程中，比如rtos文件夹下面的文件，还有一些头文件，所以直接指明搜索路径搜索的更全一些

TARGET_STM32F103RB这个选项关系到代码移植，我们要移植成TARGET_STM32F103RC
通过搜索我们可以找到引用这个宏定义的地方

	#elif defined(TARGET_STM32F100RB)

	#ifndef INITIAL_SP
	#define INITIAL_SP              (0x20002000UL)
	#endif
	#ifndef OS_TASKCNT
	#define OS_TASKCNT              6
	#endif
	#ifndef OS_MAINSTKSIZE
	#define OS_MAINSTKSIZE          128
	#endif
	#ifndef OS_CLOCK
	#define OS_CLOCK                24000000
	#endif

	#elif defined(TARGET_STM32F103RB)

	#ifndef INITIAL_SP
	#define INITIAL_SP              (0x20005000UL)
	#endif
	#ifndef OS_TASKCNT
	#define OS_TASKCNT              6
	#endif
	#ifndef OS_MAINSTKSIZE
	#define OS_MAINSTKSIZE          128
	#endif
	#ifndef OS_CLOCK
	#define OS_CLOCK                72000000
	#endif
在后面添加

	#elif defined(TARGET_STM32F103RC)

	#ifndef INITIAL_SP
	#define INITIAL_SP              (0x2000C000UL)
	#endif
	#ifndef OS_TASKCNT
	#define OS_TASKCNT              6
	#endif
	#ifndef OS_MAINSTKSIZE
	#define OS_MAINSTKSIZE          128
	#endif
	#ifndef OS_CLOCK
	#define OS_CLOCK                72000000
	#endif
好了至此移植彻底完成了。

  [mbed在线编译器]: https://developer.mbed.org/
  [Mbed源码仓库]: https://github.com/ARMmbed/mbed-os
  [Stm32f1官方hal库]:http://www.st.com/content/st_com/en/products/embedded-software/mcus-embedded-software/stm32-embedded-software/stm32cube-embedded-software/stm32cubef1.html
  
  [1]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic1.png
  [2]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic2.png
  [3]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic3.png
  [4]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic4.png
  [5]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic5.png
  [6]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic6.png
  [7]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic7.png
  [8]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic8.png
  [9]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic9.png
  [10]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic10.png
  [11]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic11.png
  [12]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic12.png
  [13]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic13.png
  [14]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic14.png
  [15]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic15.png
  [16]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic16.png
  [17]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic17.png
  [18]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic18.png
  [19]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic19.png
  [20]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic20.png
  [21]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic21.png
  [22]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic22.png
  [23]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic23.png
  [24]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic24.png
  [25]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic25.png
  [26]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic26.png
  [27]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic27.png
  [28]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic28.png
  [29]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic29.png
  [30]: https://raw.githubusercontent.com/qiuzhiqian/MyTarget_STM32F103RC_Mbed_Demo1/master/doc/pic/pic30.png
