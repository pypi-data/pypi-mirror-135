#ifdef METAL
#define N1 p_CONSTANT_BUFFER_UINT[CInd_N1]
#define N2 p_CONSTANT_BUFFER_UINT[CInd_N2]
#define N3 p_CONSTANT_BUFFER_UINT[CInd_N3]
#define Limit_I_low_PML p_CONSTANT_BUFFER_UINT[CInd_Limit_I_low_PML]
#define Limit_J_low_PML p_CONSTANT_BUFFER_UINT[CInd_Limit_J_low_PML]
#define Limit_K_low_PML p_CONSTANT_BUFFER_UINT[CInd_Limit_K_low_PML]
#define Limit_I_up_PML p_CONSTANT_BUFFER_UINT[CInd_Limit_I_up_PML]
#define Limit_J_up_PML p_CONSTANT_BUFFER_UINT[CInd_Limit_J_up_PML]
#define Limit_K_up_PML p_CONSTANT_BUFFER_UINT[CInd_Limit_K_up_PML]
#define SizeCorrI p_CONSTANT_BUFFER_UINT[CInd_SizeCorrI]
#define SizeCorrJ p_CONSTANT_BUFFER_UINT[CInd_SizeCorrJ]
#define SizeCorrK p_CONSTANT_BUFFER_UINT[CInd_SizeCorrK]
#define PML_Thickness p_CONSTANT_BUFFER_UINT[CInd_PML_Thickness]
#define NumberSources p_CONSTANT_BUFFER_UINT[CInd_NumberSources]
#define LengthSource p_CONSTANT_BUFFER_UINT[CInd_LengthSource]
#define NumberSensors p_CONSTANT_BUFFER_UINT[CInd_NumberSensors]
#define TimeSteps p_CONSTANT_BUFFER_UINT[CInd_TimeSteps]

#define SizePML p_CONSTANT_BUFFER_UINT[CInd_SizePML]
#define SizePMLxp1 p_CONSTANT_BUFFER_UINT[CInd_SizePMLxp1]
#define SizePMLyp1 p_CONSTANT_BUFFER_UINT[CInd_SizePMLyp1]
#define SizePMLzp1 p_CONSTANT_BUFFER_UINT[CInd_SizePMLzp1]
#define SizePMLxp1yp1zp1 p_CONSTANT_BUFFER_UINT[CInd_SizePMLxp1yp1zp1]
#define ZoneCount p_CONSTANT_BUFFER_UINT[CInd_ZoneCount]

#define SelRMSorPeak p_CONSTANT_BUFFER_UINT[CInd_SelRMSorPeak]
#define SelMapsRMSPeak p_CONSTANT_BUFFER_UINT[CInd_SelMapsRMSPeak]
#define IndexRMSPeak_ALLV p_CONSTANT_BUFFER_UINT[CInd_IndexRMSPeak_ALLV]
#define IndexRMSPeak_Vx p_CONSTANT_BUFFER_UINT[CInd_IndexRMSPeak_Vx]
#define IndexRMSPeak_Vy p_CONSTANT_BUFFER_UINT[CInd_IndexRMSPeak_Vy]
#define IndexRMSPeak_Vz p_CONSTANT_BUFFER_UINT[CInd_IndexRMSPeak_Vz]
#define IndexRMSPeak_Sigmaxx p_CONSTANT_BUFFER_UINT[CInd_IndexRMSPeak_Sigmaxx]
#define IndexRMSPeak_Sigmayy p_CONSTANT_BUFFER_UINT[CInd_IndexRMSPeak_Sigmayy]
#define IndexRMSPeak_Sigmazz p_CONSTANT_BUFFER_UINT[CInd_IndexRMSPeak_Sigmazz]
#define IndexRMSPeak_Sigmaxy p_CONSTANT_BUFFER_UINT[CInd_IndexRMSPeak_Sigmaxy]
#define IndexRMSPeak_Sigmaxz p_CONSTANT_BUFFER_UINT[CInd_IndexRMSPeak_Sigmaxz]
#define IndexRMSPeak_Sigmayz p_CONSTANT_BUFFER_UINT[CInd_IndexRMSPeak_Sigmayz]
#define IndexRMSPeak_Pressure p_CONSTANT_BUFFER_UINT[CInd_IndexRMSPeak_Pressure]
#define NumberSelRMSPeakMaps p_CONSTANT_BUFFER_UINT[CInd_NumberSelRMSPeakMaps]

#define SelMapsSensors p_CONSTANT_BUFFER_UINT[CInd_SelMapsSensors]
#define IndexSensor_ALLV p_CONSTANT_BUFFER_UINT[CInd_IndexSensor_ALLV]
#define IndexSensor_Vx p_CONSTANT_BUFFER_UINT[CInd_IndexSensor_Vx]
#define IndexSensor_Vy p_CONSTANT_BUFFER_UINT[CInd_IndexSensor_Vy]
#define IndexSensor_Vz p_CONSTANT_BUFFER_UINT[CInd_IndexSensor_Vz]
#define IndexSensor_Sigmaxx p_CONSTANT_BUFFER_UINT[CInd_IndexSensor_Sigmaxx]
#define IndexSensor_Sigmayy p_CONSTANT_BUFFER_UINT[CInd_IndexSensor_Sigmayy]
#define IndexSensor_Sigmazz p_CONSTANT_BUFFER_UINT[CInd_IndexSensor_Sigmazz]
#define IndexSensor_Sigmaxy p_CONSTANT_BUFFER_UINT[CInd_IndexSensor_Sigmaxy]
#define IndexSensor_Sigmaxz p_CONSTANT_BUFFER_UINT[CInd_IndexSensor_Sigmaxz]
#define IndexSensor_Sigmayz p_CONSTANT_BUFFER_UINT[CInd_IndexSensor_Sigmayz]
#define IndexSensor_Pressure p_CONSTANT_BUFFER_UINT[CInd_IndexSensor_Pressure]
#define NumberSelSensorMaps p_CONSTANT_BUFFER_UINT[CInd_NumberSelSensorMaps]
#define SensorSubSampling p_CONSTANT_BUFFER_UINT[CInd_SensorSubSampling]
#define SensorStart p_CONSTANT_BUFFER_UINT[CInd_SensorStart]
#define nStep p_CONSTANT_BUFFER_UINT[CInd_nStep]
#define CurrSnap p_CONSTANT_BUFFER_UINT[CInd_CurrSnap]
#define TypeSource p_CONSTANT_BUFFER_UINT[CInd_TypeSource]
#define SelK p_CONSTANT_BUFFER_UINT[CInd_SelK]

#define DT p_CONSTANT_BUFFER_MEX[CInd_DT]
#define InvDXDTplus_pr (p_CONSTANT_BUFFER_MEX + CInd_InvDXDTplus)
#define DXDTminus_pr (p_CONSTANT_BUFFER_MEX + CInd_DXDTminus)
#define InvDXDTplushp_pr (p_CONSTANT_BUFFER_MEX + CInd_InvDXDTplushp)
#define DXDTminushp_pr (p_CONSTANT_BUFFER_MEX + CInd_DXDTminushp)

#define __def_MEX_VAR_0(__NameVar)  (&p_MEX_BUFFER_0[ ((unsigned long) (p_INDEX_MEX[CInd_ ##__NameVar *2])) | (((unsigned long) (p_INDEX_MEX[CInd_ ##__NameVar*2+1]))<<32) ]) 
#define __def_MEX_VAR_1(__NameVar)  (&p_MEX_BUFFER_1[ ((unsigned long) (p_INDEX_MEX[CInd_ ##__NameVar *2])) | (((unsigned long) (p_INDEX_MEX[CInd_ ##__NameVar*2+1]))<<32) ]) 
#define __def_MEX_VAR_2(__NameVar)  (&p_MEX_BUFFER_2[ ((unsigned long) (p_INDEX_MEX[CInd_ ##__NameVar *2])) | (((unsigned long) (p_INDEX_MEX[CInd_ ##__NameVar*2+1]))<<32) ]) 
#define __def_MEX_VAR_3(__NameVar)  (&p_MEX_BUFFER_3[ ((unsigned long) (p_INDEX_MEX[CInd_ ##__NameVar *2])) | (((unsigned long) (p_INDEX_MEX[CInd_ ##__NameVar*2+1]))<<32) ]) 
#define __def_MEX_VAR_4(__NameVar)  (&p_MEX_BUFFER_4[ ((unsigned long) (p_INDEX_MEX[CInd_ ##__NameVar *2])) | (((unsigned long) (p_INDEX_MEX[CInd_ ##__NameVar*2+1]))<<32) ]) 
#define __def_MEX_VAR_5(__NameVar)  (&p_MEX_BUFFER_5[ ((unsigned long) (p_INDEX_MEX[CInd_ ##__NameVar *2])) | (((unsigned long) (p_INDEX_MEX[CInd_ ##__NameVar*2+1]))<<32) ]) 
#define __def_MEX_VAR_6(__NameVar)  (&p_MEX_BUFFER_6[ ((unsigned long) (p_INDEX_MEX[CInd_ ##__NameVar *2])) | (((unsigned long) (p_INDEX_MEX[CInd_ ##__NameVar*2+1]))<<32) ]) 
#define __def_MEX_VAR_7(__NameVar)  (&p_MEX_BUFFER_7[ ((unsigned long) (p_INDEX_MEX[CInd_ ##__NameVar *2])) | (((unsigned long) (p_INDEX_MEX[CInd_ ##__NameVar*2+1]))<<32) ]) 
#define __def_MEX_VAR_8(__NameVar)  (&p_MEX_BUFFER_8[ ((unsigned long) (p_INDEX_MEX[CInd_ ##__NameVar *2])) | (((unsigned long) (p_INDEX_MEX[CInd_ ##__NameVar*2+1]))<<32) ]) 
#define __def_MEX_VAR_9(__NameVar)  (&p_MEX_BUFFER_9[ ((unsigned long) (p_INDEX_MEX[CInd_ ##__NameVar *2])) | (((unsigned long) (p_INDEX_MEX[CInd_ ##__NameVar*2+1]))<<32) ]) 
#define __def_MEX_VAR_10(__NameVar)  (&p_MEX_BUFFER_10[ ((unsigned long) (p_INDEX_MEX[CInd_ ##__NameVar *2])) | (((unsigned long) (p_INDEX_MEX[CInd_ ##__NameVar*2+1]))<<32) ]) 
#define __def_MEX_VAR_11(__NameVar)  (&p_MEX_BUFFER_11[ ((unsigned long) (p_INDEX_MEX[CInd_ ##__NameVar *2])) | (((unsigned long) (p_INDEX_MEX[CInd_ ##__NameVar*2+1]))<<32) ]) 

#define __def_UINT_VAR(__NameVar)  (&p_UINT_BUFFER[ ((unsigned long) (p_INDEX_UINT[CInd_ ##__NameVar*2])) | (((unsigned long) (p_INDEX_UINT[CInd_ ##__NameVar*2+1]))<<32) ])

// #define __def_MEX_VAR(__NameVar)  (&p_MEX_BUFFER[ p_INDEX_MEX[CInd_ ##__NameVar ]]) 
// #define __def_UINT_VAR(__NameVar)  (&p_UINT_BUFFER[ p_INDEX_UINT[CInd_ ##__NameVar]])


#define k_V_x_x_pr  __def_MEX_VAR_0(V_x_x)
#define k_V_y_x_pr  __def_MEX_VAR_0(V_y_x)
#define k_V_z_x_pr  __def_MEX_VAR_0(V_z_x)
#define k_V_x_y_pr  __def_MEX_VAR_0(V_x_y)
#define k_V_y_y_pr  __def_MEX_VAR_0(V_y_y)
#define k_V_z_y_pr  __def_MEX_VAR_0(V_z_y)
#define k_V_x_z_pr  __def_MEX_VAR_0(V_x_z)
#define k_V_y_z_pr  __def_MEX_VAR_0(V_y_z)
#define k_V_z_z_pr  __def_MEX_VAR_0(V_z_z)

#define k_Vx_pr  __def_MEX_VAR_1(Vx)
#define k_Vy_pr  __def_MEX_VAR_1(Vy)
#define k_Vz_pr  __def_MEX_VAR_1(Vz)

#define k_Rxx_pr  __def_MEX_VAR_2(Rxx)
#define k_Ryy_pr  __def_MEX_VAR_2(Ryy)
#define k_Rzz_pr  __def_MEX_VAR_2(Rzz)

#define k_Rxy_pr  __def_MEX_VAR_3(Rxy)
#define k_Rxz_pr  __def_MEX_VAR_3(Rxz)
#define k_Ryz_pr  __def_MEX_VAR_3(Ryz)

#define k_Sigma_x_xx_pr  __def_MEX_VAR_4(Sigma_x_xx)
#define k_Sigma_y_xx_pr  __def_MEX_VAR_4(Sigma_y_xx)
#define k_Sigma_z_xx_pr  __def_MEX_VAR_4(Sigma_z_xx)
#define k_Sigma_x_yy_pr  __def_MEX_VAR_4(Sigma_x_yy)
#define k_Sigma_y_yy_pr  __def_MEX_VAR_4(Sigma_y_yy)
#define k_Sigma_z_yy_pr  __def_MEX_VAR_4(Sigma_z_yy)
#define k_Sigma_x_zz_pr  __def_MEX_VAR_4(Sigma_x_zz)
#define k_Sigma_y_zz_pr  __def_MEX_VAR_4(Sigma_y_zz)

#define k_Sigma_z_zz_pr  __def_MEX_VAR_5(Sigma_z_zz)
#define k_Sigma_x_xy_pr  __def_MEX_VAR_5(Sigma_x_xy)
#define k_Sigma_y_xy_pr  __def_MEX_VAR_5(Sigma_y_xy)
#define k_Sigma_x_xz_pr  __def_MEX_VAR_5(Sigma_x_xz)
#define k_Sigma_z_xz_pr  __def_MEX_VAR_5(Sigma_z_xz)
#define k_Sigma_y_yz_pr  __def_MEX_VAR_5(Sigma_y_yz)
#define k_Sigma_z_yz_pr  __def_MEX_VAR_5(Sigma_z_yz)

#define k_Sigma_xy_pr  __def_MEX_VAR_6(Sigma_xy)
#define k_Sigma_xz_pr  __def_MEX_VAR_6(Sigma_xz)
#define k_Sigma_yz_pr  __def_MEX_VAR_6(Sigma_yz)

#define k_Sigma_xx_pr  __def_MEX_VAR_7(Sigma_xx)
#define k_Sigma_yy_pr  __def_MEX_VAR_7(Sigma_yy)
#define k_Sigma_zz_pr  __def_MEX_VAR_7(Sigma_zz)

#define k_SourceFunctions_pr __def_MEX_VAR_8(SourceFunctions)

#define k_LambdaMiuMatOverH_pr  __def_MEX_VAR_9(LambdaMiuMatOverH)
#define k_LambdaMatOverH_pr     __def_MEX_VAR_9(LambdaMatOverH)
#define k_MiuMatOverH_pr        __def_MEX_VAR_9(MiuMatOverH)
#define k_TauLong_pr            __def_MEX_VAR_9(TauLong)
#define k_OneOverTauSigma_pr    __def_MEX_VAR_9(OneOverTauSigma)
#define k_TauShear_pr           __def_MEX_VAR_9(TauShear)
#define k_InvRhoMatH_pr         __def_MEX_VAR_9(InvRhoMatH)
#define k_Ox_pr  __def_MEX_VAR_9(Ox)
#define k_Oy_pr  __def_MEX_VAR_9(Oy)
#define k_Oz_pr  __def_MEX_VAR_9(Oz)
#define k_Pressure_pr  __def_MEX_VAR_9(Pressure)

#define k_SqrAcc_pr  __def_MEX_VAR_10(SqrAcc)

#define k_SensorOutput_pr  __def_MEX_VAR_11(SensorOutput)

#define k_IndexSensorMap_pr  __def_UINT_VAR(IndexSensorMap)
#define k_SourceMap_pr		 __def_UINT_VAR(SourceMap)
#define k_MaterialMap_pr	 __def_UINT_VAR(MaterialMap)
#endif

#if defined(CUDA)
__global__ void StressKernel(InputDataKernel *p,unsigned int nStep, unsigned int TypeSource)
{
	const _PT i = (_PT) (blockIdx.x * blockDim.x + threadIdx.x);
    const _PT j = (_PT) (blockIdx.y * blockDim.y + threadIdx.y);
    const _PT k = (_PT) (blockIdx.z * blockDim.z + threadIdx.z);
#endif
#ifdef OPENCL
__kernel void StressKernel(
__global mexType *V_x_x_pr,
__global mexType *V_y_x_pr,
__global mexType *V_z_x_pr,
__global mexType *V_x_y_pr,
__global mexType *V_y_y_pr,
__global mexType *V_z_y_pr,
__global mexType *V_x_z_pr,
__global mexType *V_y_z_pr,
__global mexType *V_z_z_pr,
__global mexType *Vx_pr,
__global mexType *Vy_pr,
__global mexType *Vz_pr,
__global mexType *Rxx_pr,
__global mexType *Ryy_pr,
__global mexType *Rzz_pr,
__global mexType *Rxy_pr,
__global mexType *Rxz_pr,
__global mexType *Ryz_pr,
__global mexType *Sigma_x_xx_pr,
__global mexType *Sigma_y_xx_pr,
__global mexType *Sigma_z_xx_pr,
__global mexType *Sigma_x_yy_pr,
__global mexType *Sigma_y_yy_pr,
__global mexType *Sigma_z_yy_pr,
__global mexType *Sigma_x_zz_pr,
__global mexType *Sigma_y_zz_pr,
__global mexType *Sigma_z_zz_pr,
__global mexType *Sigma_x_xy_pr,
__global mexType *Sigma_y_xy_pr,
__global mexType *Sigma_x_xz_pr,
__global mexType *Sigma_z_xz_pr,
__global mexType *Sigma_y_yz_pr,
__global mexType *Sigma_z_yz_pr,
__global mexType *Sigma_xy_pr,
__global mexType *Sigma_xz_pr,
__global mexType *Sigma_yz_pr,
__global mexType *Sigma_xx_pr,
__global mexType *Sigma_yy_pr,
__global mexType *Sigma_zz_pr,
__global mexType *SourceFunctions_pr,
__global mexType * LambdaMiuMatOverH_pr,
__global mexType * LambdaMatOverH_pr,
__global mexType * MiuMatOverH_pr,
__global mexType * TauLong_pr,
__global mexType * OneOverTauSigma_pr,
__global mexType * TauShear_pr,
__global mexType * InvRhoMatH_pr,
__global mexType * SqrAcc_pr,
__global unsigned int * MaterialMap_pr,
__global unsigned int * SourceMap_pr,
__global mexType * Ox_pr,
__global mexType * Oy_pr,
__global mexType * Oz_pr,
__global mexType * Pressure_pr
	, unsigned int nStep, unsigned int TypeSource)
{
  const _PT i = (_PT) get_global_id(0);
  const _PT j = (_PT) get_global_id(1);
  const _PT k = (_PT) get_global_id(2);
#endif
#ifdef METAL
kernel void StressKernel(
	const device unsigned int *p_CONSTANT_BUFFER_UINT [[ buffer(0) ]],
	const device mexType * p_CONSTANT_BUFFER_MEX [[ buffer(1) ]],
	const device unsigned int *p_INDEX_MEX [[ buffer(2) ]],
	const device unsigned int *p_INDEX_UINT [[ buffer(3) ]],
	const device unsigned int *p_UINT_BUFFER [[ buffer(4) ]],
	device mexType * p_MEX_BUFFER_0 [[ buffer(5) ]],
	device mexType * p_MEX_BUFFER_1 [[ buffer(6) ]],
	device mexType * p_MEX_BUFFER_2 [[ buffer(7) ]],
	device mexType * p_MEX_BUFFER_3 [[ buffer(8) ]],
	device mexType * p_MEX_BUFFER_4 [[ buffer(9) ]],
	device mexType * p_MEX_BUFFER_5 [[ buffer(10) ]],
	device mexType * p_MEX_BUFFER_6 [[ buffer(11) ]],
	device mexType * p_MEX_BUFFER_7 [[ buffer(12) ]],
	device mexType * p_MEX_BUFFER_8 [[ buffer(13) ]],
	device mexType * p_MEX_BUFFER_9 [[ buffer(14) ]],
	device mexType * p_MEX_BUFFER_10 [[ buffer(15) ]],
	device mexType * p_MEX_BUFFER_11 [[ buffer(16) ]],
	uint3 gid[[thread_position_in_grid]])
{
  const _PT i = (_PT) gid.x;
  const _PT j = (_PT) gid.y;
  const _PT k = (_PT) gid.z;
#endif


    if (i>N1 || j >N2  || k>N3)
		return;

    mexType Diff,value,Dx,Dy,Dz,m1,m2,m3,m4,RigidityXY=0.0,RigidityXZ=0.0,
        RigidityYZ=0.0,LambdaMiu,Miu,LambdaMiuComp,MiuComp,
        dFirstPart,OneOverTauSigma,dFirstPartForR,NextR,
            TauShearXY=0.0,TauShearXZ=0.0,TauShearYZ=0.0,
            accum_xx=0.0,accum_yy=0.0,accum_zz=0.0,
            accum_xy=0.0,accum_xz=0.0,accum_yz=0.0,
			accum_p=0.0;
#ifdef USE_2ND_ORDER_EDGES
    interface_t interfaceZ=inside, interfaceY=inside, interfaceX=inside;
#endif
   	_PT index,index2, MaterialID,source,bAttenuating=1;
	_PT CurZone;
for ( CurZone=0;CurZone<ZoneCount;CurZone++)
  {
  	if (i<N1 && j<N2 && k<N3)
  	{
      index=Ind_MaterialMap(i,j,k);
      MaterialID=ELD(MaterialMap,index);

  		m1=ELD(MiuMatOverH,MaterialID);
  #ifdef USE_2ND_ORDER_EDGES

          //if (m1!=0.0)

          {
              if (i<N1-1)
              {
                  if XOR(ELD(MiuMatOverH,EL(MaterialMap,i+1,j,k))==0.0,m1==0.0)
                      interfaceX=interfaceX|frontLine;
                  if XOR(ELD(MiuMatOverH,EL(MaterialMap,i+2,j,k))==0.0,m1==0.0)
                      interfaceX=interfaceX|frontLinep1;
              }
              if(i>0)
                  if XOR(ELD(MiuMatOverH,EL(MaterialMap,i-1,j,k))==0.0,m1==0.0)
                      interfaceX=interfaceX|backLine;
              if(i>2)
                  if XOR(ELD(MiuMatOverH,EL(MaterialMap,i-2,j,k))==0.0,m1==0.0)
                      interfaceX=interfaceX|backLinem1;

              if (j<N2-1)
              {
                  if XOR(ELD(MiuMatOverH,EL(MaterialMap,i,j+1,k))==0.0,m1==0.0)
                      interfaceY=interfaceY|frontLine;
                  if XOR(ELD(MiuMatOverH,EL(MaterialMap,i,j+2,k))==0.0,m1==0.0)
                      interfaceY=interfaceY|frontLinep1;
              }
              if(j>0)
                  if XOR(ELD(MiuMatOverH,EL(MaterialMap,i,j-1,k))==0.0,m1==0.0)
                      interfaceY=interfaceY|backLine;
              if(j>1)
                  if XOR(ELD(MiuMatOverH,EL(MaterialMap,i,j-2,k))==0.0,m1==0.0)
                      interfaceY=interfaceY|backLinem1;

              if (k<N3-1)
              {
                  if XOR(ELD(MiuMatOverH,EL(MaterialMap,i,j,k+1))==0.0,m1==0.0)
                      interfaceZ=interfaceZ|frontLine;
                  if XOR(ELD(MiuMatOverH,EL(MaterialMap,i,j,k+2))==0.0,m1==0.0)
                      interfaceZ=interfaceZ|frontLinep1;
              }
              if(k>0)
                  if XOR(ELD(MiuMatOverH,EL(MaterialMap,i,j,k-1))==0.0,m1==0.0)
                      interfaceZ=interfaceZ|backLine;
              if(k>1)
                  if XOR(ELD(MiuMatOverH,EL(MaterialMap,i,j,k-1))==0.0,m1==0.0)
                      interfaceZ=interfaceZ|backLinem1;
          }
  #endif

  		/*
          RigidityXY=m1;
          RigidityXZ=m1;
          RigidityYZ=m1;

          TauShearXY=ELD(TauShear,MaterialID);
          TauShearXZ=TauShearXY;
          TauShearYZ=TauShearXY;
          */

  		m2=ELD(MiuMatOverH,EL(MaterialMap,i+1,j,k));
  		m3=ELD(MiuMatOverH,EL(MaterialMap,i,j+1,k));
  		m4=ELD(MiuMatOverH,EL(MaterialMap,i+1,j+1,k));

   		value=m1*m2*m3*m4;
  		RigidityXY =value !=0.0 ? 4.0/(1.0/m1+1.0/m2+1.0/m3+1.0/m4):0.0;
  		TauShearXY = value!=0.0 ? 0.25*(ELD(TauShear,MaterialID) +
  							 ELD(TauShear,EL(MaterialMap,i+1,j,k)) +
  							 ELD(TauShear,EL(MaterialMap,i,j+1,k)) +
  							 ELD(TauShear,EL(MaterialMap,i+1,j+1,k)))
  							 : ELD(TauShear,MaterialID);


  		m3=ELD(MiuMatOverH,EL(MaterialMap,i,j,k+1));
  		m4=ELD(MiuMatOverH,EL(MaterialMap,i+1,j,k+1));

  		value=m1*m2*m3*m4;
  		RigidityXZ =value !=0.0 ? 4.0/(1.0/m1+1.0/m2+1.0/m3+1.0/m4):0.0;
  		TauShearXZ= value!=0.0 ? 0.25*(ELD(TauShear,MaterialID) +
  							 ELD(TauShear,EL(MaterialMap,i+1,j,k)) +
  							 ELD(TauShear,EL(MaterialMap,i,j,k+1)) +
  							 ELD(TauShear,EL(MaterialMap,i+1,j,k+1)))
  							 : ELD(TauShear,MaterialID);


  		m2=ELD(MiuMatOverH,EL(MaterialMap,i,j+1,k));
  		m4=ELD(MiuMatOverH,EL(MaterialMap,i,j+1,k+1));

          value=m1*m2*m3*m4;

  		RigidityYZ =value !=0.0 ? 4.0/(1.0/m1+1.0/m2+1.0/m3+1.0/m4):0.0;
  		TauShearYZ= value!=0.0 ? 0.25*(ELD(TauShear,MaterialID) +
  							 ELD(TauShear,EL(MaterialMap,i,j+1,k)) +
  							 ELD(TauShear,EL(MaterialMap,i,j,k+1)) +
  							 ELD(TauShear,EL(MaterialMap,i,j+1,k+1)))
  							 : ELD(TauShear,MaterialID);


  	}

  	if (IsOnPML_I(i)==1 || IsOnPML_J(j)==1 ||  IsOnPML_K(k)==1)//We are in the PML borders
  	 {
  		if (i<N1-1 && j <N2-1 && k < N3-1)
  		{


  			Diff= i>1 && i <N1-1 ? CA*(EL(Vx,i,j,k)-EL(Vx,i-1,j,k)) -
  			                       CB*(EL(Vx,i+1,j,k)-EL(Vx,i-2,j,k))
  			      : i>0 && i <N1 ? (EL(Vx,i,j,k)-EL(Vx,i-1,j,k))  :0;


  			index2=Ind_Sigma_x_xx(i,j,k);
  			ELD(Sigma_x_xx,index2) =InvDXDT_I*(
  											ELD(Sigma_x_xx,index2)*DXDT_I+
  											ELD(LambdaMiuMatOverH,MaterialID)*
  											Diff);
  			index2=Ind_Sigma_x_yy(i,j,k);
  			ELD(Sigma_x_yy,index2) =InvDXDT_I*(
  											ELD(Sigma_x_yy,index2)*DXDT_I+
  											ELD(LambdaMatOverH,MaterialID)*
  											Diff);

  			index2=Ind_Sigma_x_zz(i,j,k);
  			ELD(Sigma_x_zz,index2) =InvDXDT_I*(
  											ELD(Sigma_x_zz,index2)*DXDT_I+
  											ELD(LambdaMatOverH,MaterialID)*
  											Diff);




  			Diff= j>1 && j < N2-1 ? CA*(EL(Vy,i,j,k)-EL(Vy,i,j-1,k))-
  									CB*(EL(Vy,i,j+1,k)-EL(Vy,i,j-2,k))
  			        : j>0 && j < N2 ? EL(Vy,i,j,k)-EL(Vy,i,j-1,k):0;

  			index2=Ind_Sigma_y_xx(i,j,k);
  			ELD(Sigma_y_xx,index2) =InvDXDT_J*(
  											ELD(Sigma_y_xx,index2)*DXDT_J+
  											ELD(LambdaMatOverH,MaterialID)*
  											Diff);

  			index2=Ind_Sigma_y_yy(i,j,k);
  			ELD(Sigma_y_yy,index2) =InvDXDT_J*(
  											ELD(Sigma_y_yy,index2)*DXDT_J+
  											ELD(LambdaMiuMatOverH,MaterialID)*
  											Diff);

  			index2=Ind_Sigma_y_zz(i,j,k);
  			ELD(Sigma_y_zz,index2) =InvDXDT_J*(
  											ELD(Sigma_y_zz,index2)*DXDT_J+
  											ELD(LambdaMatOverH,MaterialID)*
  											Diff);



  			Diff= k>1 && k < N3-1 ? CA*(EL(Vz,i,j,k)-EL(Vz,i,j,k-1)) -
  									CB*(EL(Vz,i,j,k+1)-EL(Vz,i,j,k-2))
  			                       :k>0 && k < N3 ? EL(Vz,i,j,k)-EL(Vz,i,j,k-1) : 0;
  			index2=Ind_Sigma_z_xx(i,j,k);
  			ELD(Sigma_z_xx,index2) =InvDXDT_K*(
  											ELD(Sigma_z_xx,index2)*DXDT_K+
  											ELD(LambdaMatOverH,MaterialID)*
  											Diff);

  			index2=Ind_Sigma_z_yy(i,j,k);
  			ELD(Sigma_z_yy,index2) =InvDXDT_K*(
  											ELD(Sigma_z_yy,index2)*DXDT_K+
  											ELD(LambdaMatOverH,MaterialID)*
  											Diff);

  			index2=Ind_Sigma_z_zz(i,j,k);
  			ELD(Sigma_z_zz,index2) =InvDXDT_K*(
  											ELD(Sigma_z_zz,index2)*DXDT_K+
  											ELD(LambdaMiuMatOverH,MaterialID)*
  											Diff);




  			index=Ind_Sigma_xy(i,j,k);
  			index2=Ind_Sigma_x_xy(i,j,k);

  			Diff= i >0 && i<N1-2 ? CA*(EL(Vy,i+1,j,k)-EL(Vy,i,j,k)) -
  			                   CB*(EL(Vy,i+2,j,k)-EL(Vy,i-1,j,k))
  			                    :i<N1-1 ? EL(Vy,i+1,j,k)-EL(Vy,i,j,k):0;

  			ELD(Sigma_x_xy,index2) =InvDXDThp_I*(
  											ELD(Sigma_x_xy,index2)*DXDThp_I+
  											RigidityXY*
  											Diff);


  			index2=Ind_Sigma_x_xz(i,j,k);

  			Diff= i>0 && i<N1-2 ? CA*(EL(Vz,i+1,j,k)-EL(Vz,i,j,k)) -
  								  CB*(EL(Vz,i+2,j,k)-EL(Vz,i-1,j,k))
  								  :i<N1-1 ? EL(Vz,i+1,j,k)-EL(Vz,i,j,k):0;

  			ELD(Sigma_x_xz,index2) =InvDXDThp_I*(
  											ELD(Sigma_x_xz,index2)*DXDThp_I+
  											RigidityXZ*
  											Diff);


  			index=Ind_Sigma_xy(i,j,k);
  			index2=Ind_Sigma_y_xy(i,j,k);

  			Diff=j > 0 && j<N2-2 ? CA*(EL(Vx,i,j+1,k)-EL(Vx,i,j,k) )-
  			                       CB*(EL(Vx,i,j+2,k)-EL(Vx,i,j-1,k) )
  			                       :j<N2-1 ? EL(Vx,i,j+1,k)-EL(Vx,i,j,k) :0;

  			ELD(Sigma_y_xy,index2) =InvDXDThp_J*(
  											ELD(Sigma_y_xy,index2)*DXDThp_J+
  											RigidityXY*
  											Diff);

  			index2=Ind_Sigma_y_yz(i,j,k);

  			Diff=j>0 && j<N2-2 ? CA*(EL(Vz,i,j+1,k)-EL(Vz,i,j,k)) -
  							     CB*(EL(Vz,i,j+2,k)-EL(Vz,i,j-1,k))
  							     :j<N2-1 ? EL(Vz,i,j+1,k)-EL(Vz,i,j,k):0;

  			ELD(Sigma_y_yz,index2) =InvDXDThp_J*(
  											ELD(Sigma_y_yz,index2)*DXDThp_J+
  											RigidityYZ*
  											Diff);

  			index=Ind_Sigma_xy(i,j,k);

  			index2=Ind_Sigma_z_xz(i,j,k);


  			Diff=k >0 && k < N3-2 ? CA*(EL(Vx,i,j,k+1)-EL(Vx,i,j,k)) -
  			                        CB*(EL(Vx,i,j,k+2)-EL(Vx,i,j,k-1)):
                                      k < N3-1 ? EL(Vx,i,j,k+1)-EL(Vx,i,j,k) :0;

  			ELD(Sigma_z_xz,index2) =InvDXDThp_K*(
  											ELD(Sigma_z_xz,index2)*DXDThp_K+
  											RigidityXZ*
  											Diff);

  			index2=Ind_Sigma_z_yz(i,j,k);

  			Diff=k>0 && k < N3-2 ? CA*(EL(Vy,i,j,k+1)-EL(Vy,i,j,k))-
  			                       CB*(EL(Vy,i,j,k+2)-EL(Vy,i,j,k-1))
  			                       :k < N3-1 ? EL(Vy,i,j,k+1)-EL(Vy,i,j,k):0;
  			ELD(Sigma_z_yz,index2) =InvDXDThp_K*(
  											ELD(Sigma_z_yz,index2)*DXDThp_K+
  											RigidityYZ*
  											Diff);


  			index=Ind_Sigma_xx(i,j,k);
  			index2=Ind_Sigma_x_xx(i,j,k);
  			ELD(Sigma_xx,index)= ELD(Sigma_x_xx,index2) + ELD(Sigma_y_xx,index2)+ ELD(Sigma_z_xx,index2);
  			ELD(Sigma_yy,index)= ELD(Sigma_x_yy,index2) + ELD(Sigma_y_yy,index2)+ ELD(Sigma_z_yy,index2);
  			ELD(Sigma_zz,index)= ELD(Sigma_x_zz,index2) + ELD(Sigma_y_zz,index2)+ ELD(Sigma_z_zz,index2);
  		}
  		index=Ind_Sigma_xy(i,j,k);
  		index2=Ind_Sigma_x_xy(i,j,k);
  		ELD(Sigma_xy,index)= ELD(Sigma_x_xy,index2) + ELD(Sigma_y_xy,index2);
  		ELD(Sigma_xz,index)= ELD(Sigma_x_xz,index2) + ELD(Sigma_z_xz,index2);
  		ELD(Sigma_yz,index)= ELD(Sigma_y_yz,index2) + ELD(Sigma_z_yz,index2);

  	}
  	else
  	{
  		//We are in the center, no need to check any limits, the use of the PML simplify this
  		index=Ind_Sigma_xx(i,j,k);

		if (REQUIRES_2ND_ORDER_M(X))
			Dx=EL(Vx,i,j,k)-EL(Vx,i-1,j,k);
		else
			Dx=CA*(EL(Vx,i,j,k)-EL(Vx,i-1,j,k))-
				CB*(EL(Vx,i+1,j,k)-EL(Vx,i-2,j,k));

		if REQUIRES_2ND_ORDER_M(Y)
			Dy=EL(Vy,i,j,k)-EL(Vy,i,j-1,k);
		else
			Dy=CA*(EL(Vy,i,j,k)-EL(Vy,i,j-1,k))-
				CB*(EL(Vy,i,j+1,k)-EL(Vy,i,j-2,k));

		if REQUIRES_2ND_ORDER_M(Z)
			Dz=EL(Vz,i,j,k)-EL(Vz,i,j,k-1);
		else
			Dz=CA*(EL(Vz,i,j,k)-EL(Vz,i,j,k-1))-
              CB*(EL(Vz,i,j,k+1)-EL(Vz,i,j,k-2));

		
		//We will use the particle displacement to estimate the acoustic pressure, and using the conservation of mass formula
		//We can use the stress kernel as V matrices are not being modified in this kernel,
		// and the spatial derivatives are the same ones required for pressure calculation
        // partial(p)/partial(t) = \rho c^2 div(V)
        //it is important to mention that the Python function will need still to multiply the result for the maps of (speed of sound)^2 and density, 
		// and divide by the spatial step.
		EL(Pressure,i,j,k)+=DT*(Dx+Dy+Dz);
        accum_p+=EL(Pressure,i,j,k);


  		LambdaMiu=ELD(LambdaMiuMatOverH,MaterialID)*(1.0+ELD(TauLong,MaterialID));
  		Miu=2.0*ELD(MiuMatOverH,MaterialID)*(1.0+ELD(TauShear,MaterialID));
  		OneOverTauSigma=ELD(OneOverTauSigma,MaterialID);
		dFirstPart=LambdaMiu*(Dx+Dy+Dz);
		
		if (ELD(TauLong,MaterialID)!=0.0 || ELD(TauShear,MaterialID)!=0.0) // We avoid unnecessary calculations if there is no attenuation
		{
			
			LambdaMiuComp=DT*ELD(LambdaMiuMatOverH,MaterialID)*(ELD(TauLong,MaterialID)*OneOverTauSigma);
			dFirstPartForR=LambdaMiuComp*(Dx+Dy+Dz);
			MiuComp=DT*2.0*ELD(MiuMatOverH,MaterialID)*(ELD(TauShear,MaterialID)*OneOverTauSigma);
			NextR=( (1-DT*0.5*OneOverTauSigma)*ELD(Rxx,index) - dFirstPartForR + MiuComp*(Dy+Dz))
  		    	  /(1+DT*0.5*OneOverTauSigma);

			ELD(Sigma_xx,index)+=	DT*(dFirstPart - Miu*(Dy+Dz) + 0.5*(ELD(Rxx,index) + NextR));
			ELD(Rxx,index)=NextR;
		}
		else
		{
			bAttenuating=0;
			ELD(Sigma_xx,index)+=	DT*(dFirstPart - Miu*(Dy+Dz));
		}
  		
	    accum_xx+=ELD(Sigma_xx,index);

		if (bAttenuating==1)
		{
  			NextR=( (1-DT*0.5*OneOverTauSigma)*ELD(Ryy,index) - dFirstPartForR + MiuComp*(Dx+Dz))
  		    	  /(1+DT*0.5*OneOverTauSigma);
				
  			ELD(Sigma_yy,index)+=	DT*(dFirstPart - Miu*(Dx+Dz) + 0.5*(ELD(Ryy,index) + NextR));
			ELD(Ryy,index)=NextR;
		}
		else
			ELD(Sigma_yy,index)+=	DT*(dFirstPart - Miu*(Dx+Dz));
      	
		accum_yy+=ELD(Sigma_yy,index);

  		if (bAttenuating==1)
		{
			NextR=( (1-DT*0.5*OneOverTauSigma)*ELD(Rzz,index) - dFirstPartForR +MiuComp*(Dx+Dy))
				/(1+DT*0.5*OneOverTauSigma);
  			ELD(Sigma_zz,index)+=	DT*(dFirstPart - Miu*(Dx+Dy) + 0.5*(ELD(Rzz,index) + NextR));
			ELD(Rzz,index)=NextR;
		}
		else
			ELD(Sigma_zz,index)+=	DT*(dFirstPart - Miu*(Dx+Dy));

      	accum_zz+=ELD(Sigma_zz,index);

  		index=Ind_Sigma_xy(i,j,k);

  		if (RigidityXY!=0.0)
  		{
              if (REQUIRES_2ND_ORDER_P(X))
                  Dx=EL(Vy,i+1,j,k)-EL(Vy,i,j,k);
              else
                  Dx=CA*(EL(Vy,i+1,j,k)-EL(Vy,i,j,k))-
                     CB*(EL(Vy,i+2,j,k)-EL(Vy,i-1,j,k));


              if (REQUIRES_2ND_ORDER_P(Y))
                  Dx+=EL(Vx,i,j+1,k)-EL(Vx,i,j,k);
              else
                  Dx+=CA*(EL(Vx,i,j+1,k)-EL(Vx,i,j,k))-
                      CB*(EL(Vx,i,j+2,k)-EL(Vx,i,j-1,k));

  			Miu=RigidityXY*(1.0+TauShearXY);

			if (TauShearXY!=0.0)
			{
				MiuComp=RigidityXY*(TauShearXY*OneOverTauSigma);
				NextR=( (1-DT*0.5*OneOverTauSigma)*ELD(Rxy,index) - DT*MiuComp*Dx)
  		          /(1+DT*0.5*OneOverTauSigma);
				ELD(Sigma_xy,index)+= DT*(Miu*Dx + 0.5*(ELD(Rxy,index) +NextR));
				ELD(Rxy,index)=NextR;
			}
			else
				ELD(Sigma_xy,index)+= DT*(Miu*Dx );
        	
			accum_xy+=ELD(Sigma_xy,index);

  		}
        else
            ELD(Rxy,index)=0.0;


  		if (RigidityXZ!=0.0)
  		{
			if (REQUIRES_2ND_ORDER_P(X))
				Dx=EL(Vz,i+1,j,k)-EL(Vz,i,j,k);
			else
				Dx=CA*(EL(Vz,i+1,j,k)-EL(Vz,i,j,k))-
					CB*(EL(Vz,i+2,j,k)-EL(Vz,i-1,j,k));

			if (REQUIRES_2ND_ORDER_P(Z))
				Dx+=EL(Vx,i,j,k+1)-EL(Vx,i,j,k);
			else
				Dx+=CA*(EL(Vx,i,j,k+1)-EL(Vx,i,j,k))-
					CB*(EL(Vx,i,j,k+2)-EL(Vx,i,j,k-1));

	  		Miu=RigidityXZ*(1.0+TauShearXZ);

			if (TauShearXZ!=0.0)
			{
  				MiuComp=RigidityXZ*(TauShearXZ*OneOverTauSigma);
	  			NextR=( (1-DT*0.5*OneOverTauSigma)*ELD(Rxz,index) - DT*MiuComp*Dx)
  			          /(1+DT*0.5*OneOverTauSigma);
				ELD(Sigma_xz,index)+= DT*(Miu*Dx + 0.5*(ELD(Rxz,index) +NextR));
				ELD(Rxz,index)=NextR;
			}
			else
				ELD(Sigma_xz,index)+= DT*(Miu*Dx );
        	accum_xz+=ELD(Sigma_xz,index);
  			
  		}
        else
            ELD(Rxz,index)=0.0;

  		if (RigidityYZ!=0.0 )
  		{
			if (REQUIRES_2ND_ORDER_P(Y))
				Dy=EL(Vz,i,j+1,k)-EL(Vz,i,j,k);
			else
				Dy=CA*(EL(Vz,i,j+1,k)-EL(Vz,i,j,k))-
					CB*(EL(Vz,i,j+2,k)-EL(Vz,i,j-1,k));

			if (REQUIRES_2ND_ORDER_P(Z))
				Dy+=EL(Vy,i,j,k+1)-EL(Vy,i,j,k);
			else
				Dy+=CA*(EL(Vy,i,j,k+1)-EL(Vy,i,j,k))-
					CB*(EL(Vy,i,j,k+2)-EL(Vy,i,j,k-1));

  			Miu=RigidityYZ*(1.0+TauShearYZ);
			
			if (TauShearYZ!=0)
			{
				MiuComp=RigidityYZ*(TauShearYZ*OneOverTauSigma);

				NextR=( (1-DT*0.5*OneOverTauSigma)*ELD(Ryz,index) - DT*MiuComp*Dy)
					/(1+DT*0.5*OneOverTauSigma);

				ELD(Sigma_yz,index)+= DT*(Miu*Dy + 0.5*(ELD(Ryz,index) +NextR));
				ELD(Ryz,index)=NextR;
			}
			else 
				ELD(Sigma_yz,index)+= DT*(Miu*Dy );
        	accum_yz+=ELD(Sigma_yz,index);

  		}
          else
              ELD(Ryz,index)=0.0;
		
		if ((nStep < LengthSource) && TypeSource>=2) //Source is stress
  		{
  			index=IndN1N2N3(i,j,k,0);
  			source=ELD(SourceMap,index);
  			if (source>0)
  			{
  			  source--; //need to use C index
  			  value=ELD(SourceFunctions,nStep*NumberSources+source)*ELD(Ox,index); // We use Ox as mechanism to provide weighted arrays
				index=Ind_Sigma_xx(i,j,k);
                if ((TypeSource-2)==0)
                {
                    ELD(Sigma_xx,index)+=value;
                    ELD(Sigma_yy,index)+=value;
                    ELD(Sigma_zz,index)+=value;
                }
                else
                {
                   ELD(Sigma_xx,index)=value;
                   ELD(Sigma_yy,index)=value;
                   ELD(Sigma_zz,index)=value;
                }

  			}
  		}
  	}
  }
  if (IsOnPML_I(i)==0 && IsOnPML_J(j)==0 && IsOnPML_K(k)==0 && nStep>=SensorStart*SensorSubSampling)
  {
    accum_xx/=ZoneCount;
    accum_yy/=ZoneCount;
    accum_zz/=ZoneCount;
    accum_xy/=ZoneCount;
    accum_xz/=ZoneCount;
    accum_yz/=ZoneCount;

    CurZone=0;
    index=IndN1N2N3(i,j,k,0);
    index2=N1*N2*N3;

//#define _DebugPrint
#ifdef _DebugPrint
	int bDoPrint=0;
	if (i==64 && j==64 && k==117)
		bDoPrint=1;
#endif
    if ((SelRMSorPeak & SEL_RMS) ) //RMS was selected, and it is always at the location 0 of dim 5
    {
        if (IS_Sigmaxx_SELECTED(SelMapsRMSPeak))
            ELD(SqrAcc,index+index2*IndexRMSPeak_Sigmaxx)+=accum_xx*accum_xx;
        if (IS_Sigmayy_SELECTED(SelMapsRMSPeak))
            ELD(SqrAcc,index+index2*IndexRMSPeak_Sigmayy)+=accum_yy*accum_yy;
        if (IS_Sigmazz_SELECTED(SelMapsRMSPeak))
            ELD(SqrAcc,index+index2*IndexRMSPeak_Sigmazz)+=accum_zz*accum_zz;
        if (IS_Sigmaxy_SELECTED(SelMapsRMSPeak))
            ELD(SqrAcc,index+index2*IndexRMSPeak_Sigmaxy)+=accum_xy*accum_xy;
        if (IS_Sigmaxz_SELECTED(SelMapsRMSPeak))
            ELD(SqrAcc,index+index2*IndexRMSPeak_Sigmaxz)+=accum_xz*accum_xz;
        if (IS_Sigmayz_SELECTED(SelMapsRMSPeak))
            ELD(SqrAcc,index+index2*IndexRMSPeak_Sigmayz)+=accum_yz*accum_yz;
		if (IS_Pressure_SELECTED(SelMapsRMSPeak))
		{
			ELD(SqrAcc,index+index2*IndexRMSPeak_Pressure)+=accum_p*accum_p;
			#ifdef _DebugPrint
			#ifdef OPENCL
			if (bDoPrint)
				printf("Capturing RMS  Pressure %g,%g,%lu,%lu\n",ELD(SqrAcc,index+index2*IndexRMSPeak_Pressure),
							DT,index,index2*IndexRMSPeak_Pressure);
			#endif
			#endif
		}
		#ifdef _DebugPrint
		#ifdef OPENCL
		else{
		if (bDoPrint)
			printf("Capturing Pressure RMS not enabled \n");
		}
		#endif
		#endif
    }
    if ((SelRMSorPeak & SEL_RMS) && (SelRMSorPeak & SEL_PEAK) ) //If both PEAK and RMS were selected we save in the far part of the array
        index+=index2*NumberSelRMSPeakMaps;
    if (SelRMSorPeak & SEL_PEAK)
    {
        if (IS_Sigmaxx_SELECTED(SelMapsRMSPeak))
            ELD(SqrAcc,index+index2*IndexRMSPeak_Sigmaxx)=accum_xx>ELD(SqrAcc,index+index2*IndexRMSPeak_Sigmaxx) ? accum_xx: ELD(SqrAcc,index+index2*IndexRMSPeak_Sigmaxx);
        if (IS_Sigmayy_SELECTED(SelMapsRMSPeak))
            ELD(SqrAcc,index+index2*IndexRMSPeak_Sigmayy)=accum_yy>ELD(SqrAcc,index+index2*IndexRMSPeak_Sigmayy) ? accum_yy: ELD(SqrAcc,index+index2*IndexRMSPeak_Sigmayy);
        if (IS_Sigmazz_SELECTED(SelMapsRMSPeak))
            ELD(SqrAcc,index+index2*IndexRMSPeak_Sigmazz)=accum_zz>ELD(SqrAcc,index+index2*IndexRMSPeak_Sigmazz) ? accum_zz: ELD(SqrAcc,index+index2*IndexRMSPeak_Sigmazz);
        if (IS_Sigmaxy_SELECTED(SelMapsRMSPeak))
            ELD(SqrAcc,index+index2*IndexRMSPeak_Sigmaxy)=accum_xy>ELD(SqrAcc,index+index2*IndexRMSPeak_Sigmaxy) ? accum_xy: ELD(SqrAcc,index+index2*IndexRMSPeak_Sigmaxy);
        if (IS_Sigmaxz_SELECTED(SelMapsRMSPeak))
            ELD(SqrAcc,index+index2*IndexRMSPeak_Sigmaxz)=accum_xz>ELD(SqrAcc,index+index2*IndexRMSPeak_Sigmaxz) ? accum_xz: ELD(SqrAcc,index+index2*IndexRMSPeak_Sigmaxz);
        if (IS_Sigmayz_SELECTED(SelMapsRMSPeak))
            ELD(SqrAcc,index+index2*IndexRMSPeak_Sigmayz)=accum_yz>ELD(SqrAcc,index+index2*IndexRMSPeak_Sigmayz) ? accum_yz: ELD(SqrAcc,index+index2*IndexRMSPeak_Sigmayz);
		if (IS_Pressure_SELECTED(SelMapsRMSPeak))
		{
			ELD(SqrAcc,index+index2*IndexRMSPeak_Pressure)=accum_p > ELD(SqrAcc,index+index2*IndexRMSPeak_Pressure) ? accum_p :ELD(SqrAcc,index+index2*IndexRMSPeak_Pressure);
			#ifdef _DebugPrint
			#ifdef OPENCL
			if (bDoPrint)
				printf("Capturing peak  Pressure %g,%g\n",ELD(SqrAcc,index+index2*IndexRMSPeak_Pressure),DT);
			#endif
			#endif
		}
		#ifdef _DebugPrint
		#ifdef OPENCL
		else
		{
		if (bDoPrint)
			printf("Capturing Pressure Peak not enabled \n");
		}
		#endif
		#endif
    }

  }
}

#if defined(CUDA)
__global__ void ParticleKernel(InputDataKernel * p,
			unsigned int nStep,unsigned int TypeSource)
{
	const _PT i = (_PT) (blockIdx.x * blockDim.x + threadIdx.x);
    const _PT j = (_PT) (blockIdx.y * blockDim.y + threadIdx.y);
    const _PT k = (_PT) (blockIdx.z * blockDim.z + threadIdx.z);
#endif
#ifdef OPENCL
__kernel void ParticleKernel(
__global mexType *V_x_x_pr,
__global mexType *V_y_x_pr,
__global mexType *V_z_x_pr,
__global mexType *V_x_y_pr,
__global mexType *V_y_y_pr,
__global mexType *V_z_y_pr,
__global mexType *V_x_z_pr,
__global mexType *V_y_z_pr,
__global mexType *V_z_z_pr,
__global mexType *Vx_pr,
__global mexType *Vy_pr,
__global mexType *Vz_pr,
__global mexType *Rxx_pr,
__global mexType *Ryy_pr,
__global mexType *Rzz_pr,
__global mexType *Rxy_pr,
__global mexType *Rxz_pr,
__global mexType *Ryz_pr,
__global mexType *Sigma_x_xx_pr,
__global mexType *Sigma_y_xx_pr,
__global mexType *Sigma_z_xx_pr,
__global mexType *Sigma_x_yy_pr,
__global mexType *Sigma_y_yy_pr,
__global mexType *Sigma_z_yy_pr,
__global mexType *Sigma_x_zz_pr,
__global mexType *Sigma_y_zz_pr,
__global mexType *Sigma_z_zz_pr,
__global mexType *Sigma_x_xy_pr,
__global mexType *Sigma_y_xy_pr,
__global mexType *Sigma_x_xz_pr,
__global mexType *Sigma_z_xz_pr,
__global mexType *Sigma_y_yz_pr,
__global mexType *Sigma_z_yz_pr,
__global mexType *Sigma_xy_pr,
__global mexType *Sigma_xz_pr,
__global mexType *Sigma_yz_pr,
__global mexType *Sigma_xx_pr,
__global mexType *Sigma_yy_pr,
__global mexType *Sigma_zz_pr,
__global mexType *SourceFunctions_pr,
__global mexType * LambdaMiuMatOverH_pr,
__global mexType * LambdaMatOverH_pr,
__global mexType * MiuMatOverH_pr,
__global mexType * TauLong_pr,
__global mexType * OneOverTauSigma_pr,
__global mexType * TauShear_pr,
__global mexType * InvRhoMatH_pr,
__global mexType * SqrAcc_pr,
__global unsigned int * MaterialMap_pr,
__global unsigned int * SourceMap_pr,
__global mexType * Ox_pr,
__global mexType * Oy_pr,
__global mexType * Oz_pr,
__global mexType * Pressure_pr
	, unsigned int nStep,
	unsigned int TypeSource)
{
	const _PT i = (_PT) get_global_id(0);
	const _PT j = (_PT) get_global_id(1);
	const _PT k = (_PT) get_global_id(2);
#endif
#ifdef METAL
kernel void ParticleKernel(
	const device unsigned int *p_CONSTANT_BUFFER_UINT [[ buffer(0) ]],
	const device mexType * p_CONSTANT_BUFFER_MEX [[ buffer(1) ]],
	const device unsigned int *p_INDEX_MEX [[ buffer(2) ]],
	const device unsigned int *p_INDEX_UINT [[ buffer(3) ]],
	const device unsigned int *p_UINT_BUFFER [[ buffer(4) ]],
	device mexType * p_MEX_BUFFER_0 [[ buffer(5) ]],
	device mexType * p_MEX_BUFFER_1 [[ buffer(6) ]],
	device mexType * p_MEX_BUFFER_2 [[ buffer(7) ]],
	device mexType * p_MEX_BUFFER_3 [[ buffer(8) ]],
	device mexType * p_MEX_BUFFER_4 [[ buffer(9) ]],
	device mexType * p_MEX_BUFFER_5 [[ buffer(10) ]],
	device mexType * p_MEX_BUFFER_6 [[ buffer(11) ]],
	device mexType * p_MEX_BUFFER_7 [[ buffer(12) ]],
	device mexType * p_MEX_BUFFER_8 [[ buffer(13) ]],
	device mexType * p_MEX_BUFFER_9 [[ buffer(14) ]],
	device mexType * p_MEX_BUFFER_10 [[ buffer(15) ]],
	device mexType * p_MEX_BUFFER_11 [[ buffer(16) ]],
	uint3 gid[[thread_position_in_grid]])

{
	const _PT i = (_PT) gid.x;
	const _PT j = (_PT) gid.y;
	const _PT k = (_PT) gid.z;
#endif

    if (i>N1 || j >N2  || k>N3)
		return;


#ifdef USE_2ND_ORDER_EDGES
	interface_t interfaceZ=inside, interfaceY=inside, interfaceX=inside;
#endif
    _PT index,index2, CurZone,source;
	mexType AvgInvRhoI,AvgInvRhoJ,AvgInvRhoK,Dx,Dy,Dz,Diff,value,accum_x=0.0,accum_y=0.0,accum_z=0.0;
			//accum_p=0.0;

	for (   CurZone=0;CurZone<ZoneCount;CurZone++)
		if (i<N1 && j<N2 && k<N3)
			{

		  if (IsOnPML_I(i)==1 || IsOnPML_J(j)==1 || IsOnPML_K(k)==1)
			{
				index=Ind_MaterialMap(i,j,k);
				AvgInvRhoI=ELD(InvRhoMatH,ELD(MaterialMap,index));
				//In the PML
				// For coeffs. for V_x
				if (i<N1-1 && j <N2-1 && k<N3-1)
				{
					index=Ind_V_x_x(i,j,k);


		            Diff= i>0 && i<N1-2 ? CA*(EL(Sigma_xx,i+1,j,k)-EL(Sigma_xx,i,j,k))-
		                                  CB*(EL(Sigma_xx,i+2,j,k)-EL(Sigma_xx,i-1,j,k))
					                      :i<N1-1 ? EL(Sigma_xx,i+1,j,k)-EL(Sigma_xx,i,j,k):0;

					ELD(V_x_x,index) =InvDXDThp_I*(ELD(V_x_x,index)*DXDThp_I+
													AvgInvRhoI*
													Diff);
					index=Ind_V_y_x(i,j,k);
					Diff= j>1 && j<N2-1 ? CA*(EL(Sigma_xy,i,j,k)-EL(Sigma_xy,i,j-1,k))-
					                      CB*(EL(Sigma_xy,i,j+1,k)-EL(Sigma_xy,i,j-2,k))
					                      :j>0 && j<N2 ? EL(Sigma_xy,i,j,k)-EL(Sigma_xy,i,j-1,k):0;

					ELD(V_y_x,index) =InvDXDT_J*(
													ELD(V_y_x,index)*DXDT_J+
													AvgInvRhoI*
													Diff);
					index=Ind_V_z_x(i,j,k);
					Diff= k >1 && k < N3-1 ? CA*( EL(Sigma_xz,i,j,k)-EL(Sigma_xz,i,j,k-1))-
					                         CB*( EL(Sigma_xz,i,j,k+1)-EL(Sigma_xz,i,j,k-2)) :
		                                     k >0 && k < N3 ?  EL(Sigma_xz,i,j,k)-EL(Sigma_xz,i,j,k-1):0;

					ELD(V_z_x,index) =InvDXDT_K*(
													ELD(V_z_x,index)*DXDT_K+
													AvgInvRhoI*
													Diff);


				// For coeffs. for V_y

					index=Ind_V_x_y(i,j,k);

					Diff= i>1 && i<N1-1 ? CA *(EL(Sigma_xy,i,j,k)-EL(Sigma_xy,i-1,j,k)) -
					                      CB *(EL(Sigma_xy,i+1,j,k)-EL(Sigma_xy,i-2,j,k))
					                      :i>0 && i<N1 ? EL(Sigma_xy,i,j,k)-EL(Sigma_xy,i-1,j,k):0;

					ELD(V_x_y,index) =InvDXDT_I*(
													ELD(V_x_y,index)*DXDT_I+
													AvgInvRhoI*
													Diff);
					index=Ind_V_y_y(i,j,k);
					Diff= j>0 && j < N2-2 ? CA*( EL(Sigma_yy,i,j+1,k)-EL(Sigma_yy,i,j,k)) -
					                        CB*( EL(Sigma_yy,i,j+2,k)-EL(Sigma_yy,i,j-1,k))
					                        :j < N2-1 ? EL(Sigma_yy,i,j+1,k)-EL(Sigma_yy,i,j,k):0;

					ELD(V_y_y,index) =InvDXDThp_J*(
												ELD(V_y_y,index)*DXDThp_J+
												AvgInvRhoI*
												Diff);
					index=Ind_V_y_z(i,j,k);

					Diff= k>1  && k <N3-1 ? CA*(EL(Sigma_yz,i,j,k)-EL(Sigma_yz,i,j,k-1) )-
					                        CB*(EL(Sigma_yz,i,j,k+1)-EL(Sigma_yz,i,j,k-2) )
					                        :k>0  && k <N3 ? EL(Sigma_yz,i,j,k)-EL(Sigma_yz,i,j,k-1):0;

					ELD(V_z_y,index) =InvDXDT_K*(
												ELD(V_z_y,index)*DXDT_K+
												AvgInvRhoI*
												Diff);

					index=Ind_V_x_z(i,j,k);

					Diff= i> 1 && i <N1-1 ? CA*( EL(Sigma_xz,i,j,k)-EL(Sigma_xz,i-1,j,k)) -
					                        CB*( EL(Sigma_xz,i+1,j,k)-EL(Sigma_xz,i-2,j,k))
					                        :i> 0 && i <N1 ? EL(Sigma_xz,i,j,k)-EL(Sigma_xz,i-1,j,k):0;

					ELD(V_x_z,index) =InvDXDT_I*(
													ELD(V_x_z,index)*DXDT_I+
													AvgInvRhoI*
													Diff);
					index=Ind_V_y_z(i,j,k);

					Diff= j>1 && j<N2-1 ? CA*(EL(Sigma_yz,i,j,k)-EL(Sigma_yz,i,j-1,k)) -
					                      CB*(EL(Sigma_yz,i,j+1,k)-EL(Sigma_yz,i,j-2,k)):
		                                  j>0 && j<N2 ? EL(Sigma_yz,i,j,k)-EL(Sigma_yz,i,j-1,k):0;

					ELD(V_y_z,index) =InvDXDT_J*(
												ELD(V_y_z,index)*DXDT_J+
												AvgInvRhoI*
												Diff);
					index=Ind_V_z_z(i,j,k);

					Diff= k>0 && k< N3-2 ? CA*(EL(Sigma_zz,i,j,k+1)-EL(Sigma_zz,i,j,k) )-
					                       CB*(EL(Sigma_zz,i,j,k+2)-EL(Sigma_zz,i,j,k-1) ):
		                                   k< N3-1 ? EL(Sigma_zz,i,j,k+1)-EL(Sigma_zz,i,j,k) :0;

					ELD(V_z_z,index) =InvDXDThp_K*(
												ELD(V_z_z,index)*DXDThp_K+
												AvgInvRhoI*
												Diff);
				 }

				 //We add now for Vx, Vy, Vz

				if ( j <N2 && k < N3)
				{
				   index=Ind_V_x(i,j,k);
				   index2=Ind_V_x_x(i,j,k);
				   ELD(Vx,index)=ELD(V_x_x,index2)+ELD(V_y_x,index2)+ELD(V_z_x,index2);
				}
				if (i<N1 && k < N3 )
				{
					index=Ind_V_y(i,j,k);
					index2=Ind_V_y_y(i,j,k);
					ELD(Vy,index)=ELD(V_x_y,index2)+ELD(V_y_y,index2)+ELD(V_z_y,index2);
				}
				if (i<N1 && j < N2 )
				{
					index=Ind_V_z(i,j,k);
					index2=Ind_V_z_z(i,j,k);
					ELD(Vz,index)=ELD(V_x_z,index2)+ELD(V_y_z,index2)+ELD(V_z_z,index2);
				}
			}
			else
			{
				index=Ind_MaterialMap(i,j,k);

				#ifdef USE_2ND_ORDER_EDGES
						unsigned int m1=ELD(MiuMatOverH,EL(MaterialMap,i,j,k));
						if XOR(ELD(MiuMatOverH,EL(MaterialMap,i+2,j,k))==0.0,m1== 0.0)
							interfaceX=interfaceX|frontLinep1;
						if XOR(ELD(MiuMatOverH,EL(MaterialMap,i+1,j,k))==0.0,m1 ==0.0)
							interfaceX=interfaceX|frontLine;
						if XOR(ELD(MiuMatOverH,EL(MaterialMap,i-1,j,k))==0.0,m1 ==0.0)
							interfaceX=interfaceX|backLine;
						if XOR(ELD(MiuMatOverH,EL(MaterialMap,i,j+2,k))==0.0,m1== 0.0)
							interfaceY=interfaceY|frontLinep1;
						if XOR(ELD(MiuMatOverH,EL(MaterialMap,i,j+1,k))==0.0,m1 ==0.0)
							interfaceY=interfaceY|frontLine;
						if XOR(ELD(MiuMatOverH,EL(MaterialMap,i,j-1,k))==0.0,m1 ==0.0)
							interfaceY=interfaceY|backLine;

						if XOR(ELD(MiuMatOverH,EL(MaterialMap,i,j,k+2))==0.0 , m1== 0.0)
							interfaceZ=interfaceZ|frontLinep1;
						if XOR(ELD(MiuMatOverH,EL(MaterialMap,i,j,k+1))==0.0, m1 ==0.0)
							interfaceZ=interfaceZ|frontLine;
						if XOR(ELD(MiuMatOverH,EL(MaterialMap,i,j,k-1))==0.0, m1 ==0.0)
							interfaceZ=interfaceZ|backLine;
				#endif

				AvgInvRhoI=0.5*(ELD(InvRhoMatH,EL(MaterialMap,i+1,j,k))+ELD(InvRhoMatH,ELD(MaterialMap,index)));
				AvgInvRhoJ=0.5*(ELD(InvRhoMatH,EL(MaterialMap,i,j+1,k))+ELD(InvRhoMatH,ELD(MaterialMap,index)));
				AvgInvRhoK=0.5*(ELD(InvRhoMatH,EL(MaterialMap,i,j,k+1))+ELD(InvRhoMatH,ELD(MaterialMap,index)));

				if REQUIRES_2ND_ORDER_P(X)
					Dx=EL(Sigma_xx,i+1,j,k)-EL(Sigma_xx,i,j,k);
				else
					Dx=CA*(EL(Sigma_xx,i+1,j,k)-EL(Sigma_xx,i,j,k))-
						CB*(EL(Sigma_xx,i+2,j,k)-EL(Sigma_xx,i-1,j,k));

				if REQUIRES_2ND_ORDER_P(Y)
					Dx+=EL(Sigma_xy,i,j,k)-EL(Sigma_xy,i,j-1,k);
				else
					Dx+=CA*(EL(Sigma_xy,i,j,k)-EL(Sigma_xy,i,j-1,k))-
						CB*(EL(Sigma_xy,i,j+1,k)-EL(Sigma_xy,i,j-2,k));

				if REQUIRES_2ND_ORDER_P(Z)
					Dx+=EL(Sigma_xz,i,j,k)-EL(Sigma_xz,i,j,k-1);
				else
					Dx+=CA*(EL(Sigma_xz,i,j,k)-EL(Sigma_xz,i,j,k-1))-
						CB*(EL(Sigma_xz,i,j,k+1)-EL(Sigma_xz,i,j,k-2));

				EL(Vx,i,j,k)+=DT*AvgInvRhoI*Dx;
				accum_x+=EL(Vx,i,j,k);
				//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

				if REQUIRES_2ND_ORDER_P(Y)
					Dy=EL(Sigma_yy,i,j+1,k)-EL(Sigma_yy,i,j,k);
				else
					Dy=CA*(EL(Sigma_yy,i,j+1,k)-EL(Sigma_yy,i,j,k) )-
						CB*(EL(Sigma_yy,i,j+2,k)-EL(Sigma_yy,i,j-1,k));

				if REQUIRES_2ND_ORDER_P(X)
					Dy+=EL(Sigma_xy,i,j,k)-EL(Sigma_xy,i-1,j,k);
				else
					Dy+=CA*(EL(Sigma_xy,i,j,k)-EL(Sigma_xy,i-1,j,k))-
						CB*(EL(Sigma_xy,i+1,j,k)-EL(Sigma_xy,i-2,j,k));

				if REQUIRES_2ND_ORDER_P(Z)
					Dy+=EL(Sigma_yz,i,j,k)-EL(Sigma_yz,i,j,k-1);
				else
					Dy+=CA*( EL(Sigma_yz,i,j,k)-EL(Sigma_yz,i,j,k-1))-
					CB*(EL(Sigma_yz,i,j,k+1)-EL(Sigma_yz,i,j,k-2));
				
				EL(Vy,i,j,k)+=DT*AvgInvRhoJ*Dy;
				accum_y+=EL(Vy,i,j,k);
				//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


				if REQUIRES_2ND_ORDER_P(Z)
					Dz=EL(Sigma_zz,i,j,k+1)-EL(Sigma_zz,i,j,k);
				else
					Dz=CA*(EL(Sigma_zz,i,j,k+1)-EL(Sigma_zz,i,j,k))-
						CB*( EL(Sigma_zz,i,j,k+2)-EL(Sigma_zz,i,j,k-1));

				if REQUIRES_2ND_ORDER_P(X)
					Dz+=EL(Sigma_xz,i,j,k)-EL(Sigma_xz,i-1,j,k);
				else
					Dz+=CA*(EL(Sigma_xz,i,j,k)-EL(Sigma_xz,i-1,j,k))-
					CB*(EL(Sigma_xz,i+1,j,k)-EL(Sigma_xz,i-2,j,k));

				if REQUIRES_2ND_ORDER_P(Y)
					Dz+=EL(Sigma_yz,i,j,k)-EL(Sigma_yz,i,j-1,k);
				else
					Dz+=CA*( EL(Sigma_yz,i,j,k)-EL(Sigma_yz,i,j-1,k))-
					CB*(EL(Sigma_yz,i,j+1,k)-EL(Sigma_yz,i,j-2,k));

				EL(Vz,i,j,k)+=DT*AvgInvRhoK*Dz;
				accum_z+=EL(Vz,i,j,k);

		}

  		if ((nStep < LengthSource) && TypeSource<2) //Source is particle displacement
  		{
			index=IndN1N2N3(i,j,k,0);
  			source=ELD(SourceMap,index);
  			if (source>0)
  			{
				source--; //need to use C index
  			  	value=ELD(SourceFunctions,nStep*NumberSources+source);
				if (TypeSource==0)
				{
					EL(Vx,i,j,k)+=value*ELD(Ox,index);
					EL(Vy,i,j,k)+=value*ELD(Oy,index);
					EL(Vz,i,j,k)+=value*ELD(Oz,index);
				}
				else
				{
					EL(Vx,i,j,k)=value*ELD(Ox,index);
					EL(Vy,i,j,k)=value*ELD(Oy,index);
					EL(Vz,i,j,k)=value*ELD(Oz,index);
				}

  			}
  		}

		}
		if (IsOnPML_I(i)==0 && IsOnPML_J(j)==0 && IsOnPML_K(k)==0 && nStep>=SensorStart*SensorSubSampling)
	    {
			if (ZoneCount>1)
			{
				accum_x/=ZoneCount;
				accum_y/=ZoneCount;
				accum_z/=ZoneCount;
			}
			CurZone=0;
			index=IndN1N2N3(i,j,k,0);
			index2=N1*N2*N3;
			if ((SelRMSorPeak & SEL_RMS) ) //RMS was selected, and it is always at the location 0 of dim 5
			{
				if (IS_ALLV_SELECTED(SelMapsRMSPeak))
					ELD(SqrAcc,index+index2*IndexRMSPeak_ALLV)+=accum_x*accum_x  +  accum_y*accum_y  +  accum_z*accum_z;
				if (IS_Vx_SELECTED(SelMapsRMSPeak))
					ELD(SqrAcc,index+index2*IndexRMSPeak_Vx)+=accum_x*accum_x;
				if (IS_Vy_SELECTED(SelMapsRMSPeak))
					ELD(SqrAcc,index+index2*IndexRMSPeak_Vy)+=accum_y*accum_y;
				if (IS_Vz_SELECTED(SelMapsRMSPeak))
					ELD(SqrAcc,index+index2*IndexRMSPeak_Vz)+=accum_z*accum_z;

			}
			if ((SelRMSorPeak & SEL_RMS) && (SelRMSorPeak & SEL_PEAK) ) //If both PEAK and RMS were selected we save in the far part of the array
					index+=index2*NumberSelRMSPeakMaps;
			if (SelRMSorPeak & SEL_PEAK)
			{
				if (IS_ALLV_SELECTED(SelMapsRMSPeak))
				{
					value=accum_x*accum_x  +  accum_y*accum_y  +  accum_z*accum_z; //in the Python function we will do the final sqr root`
					ELD(SqrAcc,index+index2*IndexRMSPeak_ALLV)=value > ELD(SqrAcc,index+index2*IndexRMSPeak_ALLV) ? value : ELD(SqrAcc,index+index2*IndexRMSPeak_ALLV);
				}
				if (IS_Vx_SELECTED(SelMapsRMSPeak))
						ELD(SqrAcc,index+index2*IndexRMSPeak_Vx)=accum_x > ELD(SqrAcc,index+index2*IndexRMSPeak_Vx) ? accum_x : ELD(SqrAcc,index+index2*IndexRMSPeak_Vx);
				if (IS_Vy_SELECTED(SelMapsRMSPeak))
						ELD(SqrAcc,index+index2*IndexRMSPeak_Vy)=accum_y > ELD(SqrAcc,index+index2*IndexRMSPeak_Vy) ? accum_y : ELD(SqrAcc,index+index2*IndexRMSPeak_Vy);
				if (IS_Vz_SELECTED(SelMapsRMSPeak))
						ELD(SqrAcc,index+index2*IndexRMSPeak_Vz)=accum_z > ELD(SqrAcc,index+index2*IndexRMSPeak_Vz) ? accum_z : ELD(SqrAcc,index+index2*IndexRMSPeak_Vz);

			}


		}
}


#if defined(CUDA)
__global__ void SnapShot(unsigned int SelK,mexType * Snapshots_pr,mexType * Sigma_xx_pr,mexType * Sigma_yy_pr,mexType * Sigma_zz_pr,unsigned int CurrSnap)
{
	const _PT i = (_PT) (blockIdx.x * blockDim.x + threadIdx.x);
  const _PT j = (_PT) (blockIdx.y * blockDim.y + threadIdx.y);
#endif
#ifdef OPENCL
__kernel void SnapShot(unsigned int SelK,__global mexType * Snapshots_pr,__global mexType * Sigma_xx_pr,__global mexType * Sigma_yy_pr,__global mexType * Sigma_zz_pr,unsigned int CurrSnap)
{
  const _PT i = (_PT) get_global_id(0);
  const _PT j = (_PT) get_global_id(1);
#endif
#ifdef METAL
#define Sigma_xx_pr k_Sigma_xx_pr
#define Sigma_yy_pr k_Sigma_yy_pr
#define Sigma_zz_pr k_Sigma_zz_pr

kernel void SnapShot(
	const device unsigned int *p_CONSTANT_BUFFER_UINT [[ buffer(0) ]],
	const device mexType * p_CONSTANT_BUFFER_MEX [[ buffer(1) ]],
	const device unsigned int *p_INDEX_MEX [[ buffer(2) ]],
	const device unsigned int *p_INDEX_UINT [[ buffer(3) ]],
	const device unsigned int *p_UINT_BUFFER [[ buffer(4) ]],
	device mexType * p_MEX_BUFFER_0 [[ buffer(5) ]],
	device mexType * p_MEX_BUFFER_1 [[ buffer(6) ]],
	device mexType * p_MEX_BUFFER_2 [[ buffer(7) ]],
	device mexType * p_MEX_BUFFER_3 [[ buffer(8) ]],
	device mexType * p_MEX_BUFFER_4 [[ buffer(9) ]],
	device mexType * p_MEX_BUFFER_5 [[ buffer(10) ]],
	device mexType * p_MEX_BUFFER_6 [[ buffer(11) ]],
	device mexType * p_MEX_BUFFER_7 [[ buffer(12) ]],
	device mexType * p_MEX_BUFFER_8 [[ buffer(13) ]],
	device mexType * p_MEX_BUFFER_9 [[ buffer(14) ]],
	device mexType * p_MEX_BUFFER_10 [[ buffer(15) ]],
	device mexType * p_MEX_BUFFER_11 [[ buffer(16) ]],
	device mexType * Snapshots_pr [[ buffer(17) ]],
	uint2 gid[[thread_position_in_grid]])

	{
	const _PT i = (_PT) gid.x;
	const _PT j = (_PT) gid.y;
#endif

    if (i>=N1 || j >=N2)
		return;
	mexType accum=0.0;
	for (unsigned int CurZone=0;CurZone<ZoneCount;CurZone++)
		{
			_PT index=Ind_Sigma_xx(i,j,(_PT)SelK);
			accum+=(Sigma_xx_pr[index]+Sigma_yy_pr[index]+Sigma_zz_pr[index])/3.0;

		}

		Snapshots_pr[IndN1N2Snap(i,j)+CurrSnap*N1*N2]=accum/ZoneCount;
}

#if defined(CUDA)
__global__ void SensorsKernel(InputDataKernel * p,
													  unsigned int * IndexSensorMap_pr,
														unsigned int nStep)
{
	unsigned int sj =blockIdx.x * blockDim.x + threadIdx.x;
#endif
#ifdef OPENCL
__kernel void SensorsKernel(
__global mexType *V_x_x_pr,
__global mexType *V_y_x_pr,
__global mexType *V_z_x_pr,
__global mexType *V_x_y_pr,
__global mexType *V_y_y_pr,
__global mexType *V_z_y_pr,
__global mexType *V_x_z_pr,
__global mexType *V_y_z_pr,
__global mexType *V_z_z_pr,
__global mexType *Vx_pr,
__global mexType *Vy_pr,
__global mexType *Vz_pr,
__global mexType *Rxx_pr,
__global mexType *Ryy_pr,
__global mexType *Rzz_pr,
__global mexType *Rxy_pr,
__global mexType *Rxz_pr,
__global mexType *Ryz_pr,
__global mexType *Sigma_x_xx_pr,
__global mexType *Sigma_y_xx_pr,
__global mexType *Sigma_z_xx_pr,
__global mexType *Sigma_x_yy_pr,
__global mexType *Sigma_y_yy_pr,
__global mexType *Sigma_z_yy_pr,
__global mexType *Sigma_x_zz_pr,
__global mexType *Sigma_y_zz_pr,
__global mexType *Sigma_z_zz_pr,
__global mexType *Sigma_x_xy_pr,
__global mexType *Sigma_y_xy_pr,
__global mexType *Sigma_x_xz_pr,
__global mexType *Sigma_z_xz_pr,
__global mexType *Sigma_y_yz_pr,
__global mexType *Sigma_z_yz_pr,
__global mexType *Sigma_xy_pr,
__global mexType *Sigma_xz_pr,
__global mexType *Sigma_yz_pr,
__global mexType *Sigma_xx_pr,
__global mexType *Sigma_yy_pr,
__global mexType *Sigma_zz_pr,
__global mexType *SourceFunctions_pr,
__global mexType * LambdaMiuMatOverH_pr,
__global mexType * LambdaMatOverH_pr,
__global mexType * MiuMatOverH_pr,
__global mexType * TauLong_pr,
__global mexType * OneOverTauSigma_pr,
__global mexType * TauShear_pr,
__global mexType * InvRhoMatH_pr,
__global mexType * SqrAcc_pr,
__global unsigned int * MaterialMap_pr,
__global unsigned int * SourceMap_pr,
__global mexType * Ox_pr,
__global mexType * Oy_pr,
__global mexType * Oz_pr,
__global mexType * Pressure_pr
		, __global mexType * SensorOutput_pr,
			__global unsigned int * IndexSensorMap_pr,
			unsigned int nStep)
{
	_PT sj =(_PT) get_global_id(0);
#endif
#ifdef METAL

#define IndexSensorMap_pr k_IndexSensorMap_pr

kernel void SensorsKernel(
	const device unsigned int *p_CONSTANT_BUFFER_UINT [[ buffer(0) ]],
	const device mexType * p_CONSTANT_BUFFER_MEX [[ buffer(1) ]],
	const device unsigned int *p_INDEX_MEX [[ buffer(2) ]],
	const device unsigned int *p_INDEX_UINT [[ buffer(3) ]],
	const device unsigned int *p_UINT_BUFFER [[ buffer(4) ]],
	device mexType * p_MEX_BUFFER_0 [[ buffer(5) ]],
	device mexType * p_MEX_BUFFER_1 [[ buffer(6) ]],
	device mexType * p_MEX_BUFFER_2 [[ buffer(7) ]],
	device mexType * p_MEX_BUFFER_3 [[ buffer(8) ]],
	device mexType * p_MEX_BUFFER_4 [[ buffer(9) ]],
	device mexType * p_MEX_BUFFER_5 [[ buffer(10) ]],
	device mexType * p_MEX_BUFFER_6 [[ buffer(11) ]],
	device mexType * p_MEX_BUFFER_7 [[ buffer(12) ]],
	device mexType * p_MEX_BUFFER_8 [[ buffer(13) ]],
	device mexType * p_MEX_BUFFER_9 [[ buffer(14) ]],
	device mexType * p_MEX_BUFFER_10 [[ buffer(15) ]],
	device mexType * p_MEX_BUFFER_11 [[ buffer(16) ]],
	uint gid[[thread_position_in_grid]])
{
	_PT sj = (_PT) gid;
#endif

	if (sj>=(_PT) NumberSensors)
		return;
_PT index=(((_PT)nStep)/((_PT)SensorSubSampling)-((_PT)SensorStart))*((_PT)NumberSensors)+(_PT)sj;
_PT  i,j,k;
_PT index2,index3,
    subarrsize=(((_PT)NumberSensors)*(((_PT)TimeSteps)/((_PT)SensorSubSampling)+1-((_PT)SensorStart)));
index2=IndexSensorMap_pr[sj]-1;

mexType accumX=0.0,accumY=0.0,accumZ=0.0,
        accumXX=0.0, accumYY=0.0, accumZZ=0.0,
        accumXY=0.0, accumXZ=0.0, accumYZ=0.0, accum_p=0;;
for (_PT CurZone=0;CurZone<ZoneCount;CurZone++)
  {
    k=index2/(N1*N2);
    j=index2%(N1*N2);
    i=j%(N1);
    j=j/N1;

    if (IS_ALLV_SELECTED(SelMapsSensors) || IS_Vx_SELECTED(SelMapsSensors))
        accumX+=EL(Vx,i,j,k);
    if (IS_ALLV_SELECTED(SelMapsSensors) || IS_Vy_SELECTED(SelMapsSensors))
        accumY+=EL(Vy,i,j,k);
    if (IS_ALLV_SELECTED(SelMapsSensors) || IS_Vz_SELECTED(SelMapsSensors))
        accumZ+=EL(Vz,i,j,k);

    index3=Ind_Sigma_xx(i,j,k);
  #ifdef METAL
    //No idea why in this kernel the ELD(SigmaXX...) macros do not expand correctly
    //So we go a bit more manual
  if (IS_Sigmaxx_SELECTED(SelMapsSensors))
      accumXX+=k_Sigma_xx_pr[index3];
  if (IS_Sigmayy_SELECTED(SelMapsSensors))
      accumYY+=k_Sigma_yy_pr[index3];
  if (IS_Sigmazz_SELECTED(SelMapsSensors))
      accumZZ+=k_Sigma_zz_pr[index3];
  if (IS_Pressure_SELECTED(SelMapsSensors))
      accum_p+=k_Pressure_pr[index3];
  index3=Ind_Sigma_xy(i,j,k);
  if (IS_Sigmaxy_SELECTED(SelMapsSensors))
      accumXY+=k_Sigma_xy_pr[index3];
  if (IS_Sigmaxz_SELECTED(SelMapsSensors))
      accumXZ+=k_Sigma_xz_pr[index3];
  if (IS_Sigmayz_SELECTED(SelMapsSensors))
      accumYZ+=k_Sigma_yz_pr[index3];
  
  #else
    if (IS_Sigmaxx_SELECTED(SelMapsSensors))
        accumXX+=ELD(Sigma_xx,index3);
    if (IS_Sigmayy_SELECTED(SelMapsSensors))
        accumYY+=ELD(Sigma_yy,index3);
    if (IS_Sigmazz_SELECTED(SelMapsSensors))
        accumZZ+=ELD(Sigma_zz,index3);
    if (IS_Pressure_SELECTED(SelMapsSensors))
        accum_p+=ELD(Pressure,index3);
    index3=Ind_Sigma_xy(i,j,k);
    if (IS_Sigmaxy_SELECTED(SelMapsSensors))
        accumXY+=ELD(Sigma_xy,index3);
    if (IS_Sigmaxz_SELECTED(SelMapsSensors))
        accumXZ+=ELD(Sigma_xz,index3);
    if (IS_Sigmayz_SELECTED(SelMapsSensors))
        accumYZ+=ELD(Sigma_yz,index3);
   #endif
  }
accumX/=ZoneCount;
accumY/=ZoneCount;
accumZ/=ZoneCount;
accumXX/=ZoneCount;
accumYY/=ZoneCount;
accumZZ/=ZoneCount;
accumXY/=ZoneCount;
accumXZ/=ZoneCount;
accumYZ/=ZoneCount;
accum_p/=ZoneCount;
//ELD(SensorOutput,index)=accumX*accumX+accumY*accumY+accumZ*accumZ;
if (IS_ALLV_SELECTED(SelMapsSensors))
      ELD(SensorOutput,index+subarrsize*IndexSensor_ALLV)=
        (accumX*accumX*+accumY*accumY+accumZ*accumZ);
if (IS_Vx_SELECTED(SelMapsSensors))
    ELD(SensorOutput,index+subarrsize*IndexSensor_Vx)=accumX;
if (IS_Vy_SELECTED(SelMapsSensors))
    ELD(SensorOutput,index+subarrsize*IndexSensor_Vy)=accumY;
if (IS_Vz_SELECTED(SelMapsSensors))
    ELD(SensorOutput,index+subarrsize*IndexSensor_Vz)=accumZ;
if (IS_Sigmaxx_SELECTED(SelMapsSensors))
    ELD(SensorOutput,index+subarrsize*IndexSensor_Sigmaxx)=accumXX;
if (IS_Sigmayy_SELECTED(SelMapsSensors))
    ELD(SensorOutput,index+subarrsize*IndexSensor_Sigmayy)=accumYY;
if (IS_Sigmazz_SELECTED(SelMapsSensors))
    ELD(SensorOutput,index+subarrsize*IndexSensor_Sigmazz)=accumZZ;
if (IS_Sigmaxy_SELECTED(SelMapsSensors))
    ELD(SensorOutput,index+subarrsize*IndexSensor_Sigmaxy)=accumXY;
if (IS_Sigmaxz_SELECTED(SelMapsSensors))
    ELD(SensorOutput,index+subarrsize*IndexSensor_Sigmaxz)=accumXZ;
if (IS_Sigmayz_SELECTED(SelMapsSensors))
    ELD(SensorOutput,index+subarrsize*IndexSensor_Sigmayz)=accumYZ;
if (IS_Pressure_SELECTED(SelMapsSensors))
    ELD(SensorOutput,index+subarrsize*IndexSensor_Pressure)=accum_p;

}