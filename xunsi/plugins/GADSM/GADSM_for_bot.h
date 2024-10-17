#ifndef GADSM_FOR_BOT_H
#define GADSM_FOR_BOT_H

#ifdef _WIN64
#define DECL_DLLEXPORT __declspec(dllexport)
#else
#define DECL_DLLEXPORT
#endif

#ifdef __cplusplus
extern "C"
{
#endif

    /**
     * @brief
     *
     * @param file_path 结果文件完整路径
     * @param sequence 借力序列编号 1~8
     * @param year_0 出发年份 1900~2200
     * @param year_1 到达年份 1900~2200 严格大于 year_0
     * @param C3 出发能量 km^2/s^2 大于等于 0
     * @param MS 多启动次数
     * @param pop 种群数量
     * @param gen 迭代次数
     * @return int
     * @retval 0 成功
     * @retval 1 Write result into CSV error
     * @retval -11 sequence[0] out of range
     * @retval -12 sequence[1] out of range
     * @retval -13 sequence[2] out of range
     * @retval -21 year_0 out of range
     * @retval -31 year_1 out of range
     * @retval -32 year_1 not big than year_0
     * @retval -41 C3 out of range
     */
    int GADSM_for_bot(const char *file_path, const int sequence[3], const int year_0, const int year_1, const double C3,
                      const int MS, const int pop, const int gen);

#ifdef __cplusplus
}
#endif

#endif // !GADSM_FOR_BOT_H