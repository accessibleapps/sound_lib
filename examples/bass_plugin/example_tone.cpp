// Minimal BASS file-format plugin.
//
// The input format is a small UTF-8 text file:
//
//     BASSTONE
//     <frequency in Hz>
//     <duration in milliseconds>
//
// The plugin turns that description into a mono 44.1 kHz, 16-bit sine wave.

#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>

#include "bass-addon.h"

const BASS_FUNCTIONS *bassfunc;

namespace {

constexpr DWORD kPluginVersion = 0x02040000;
constexpr DWORD kChannelType = 0x10F00;
constexpr DWORD kSampleRate = 44100;
constexpr double kTau = 6.283185307179586476925286766559;

struct ToneStream {
    DWORD frequency;
    QWORD sample_count;
    QWORD sample_position;
};

void WINAPI Free(void *instance) {
    std::free(instance);
}

QWORD WINAPI GetLength(void *instance, DWORD mode) {
    const auto *stream = static_cast<ToneStream *>(instance);
    if (mode != BASS_POS_BYTE) {
        errorn(BASS_ERROR_NOTAVAIL);
    }
    noerrorn(stream->sample_count * sizeof(short));
}

void WINAPI GetInfo(void *, BASS_CHANNELINFO *info) {
    info->ctype = kChannelType;
    info->origres = 16;
}

BOOL WINAPI CanSetPosition(void *instance, QWORD position, DWORD mode) {
    const auto *stream = static_cast<ToneStream *>(instance);
    if (static_cast<BYTE>(mode) != BASS_POS_BYTE) {
        error(BASS_ERROR_NOTAVAIL);
    }
    if (position % sizeof(short) != 0 ||
        position >= stream->sample_count * sizeof(short)) {
        error(BASS_ERROR_POSITION);
    }
    return TRUE;
}

QWORD WINAPI SetPosition(void *instance, QWORD position, DWORD) {
    auto *stream = static_cast<ToneStream *>(instance);
    stream->sample_position = position / sizeof(short);
    return position;
}

DWORD CALLBACK StreamProc(HSTREAM, void *buffer, DWORD length, void *instance) {
    auto *stream = static_cast<ToneStream *>(instance);
    const QWORD requested_samples = length / sizeof(short);
    const QWORD remaining_samples =
        stream->sample_count - stream->sample_position;
    const DWORD output_samples = static_cast<DWORD>(
        requested_samples < remaining_samples ? requested_samples
                                              : remaining_samples);

    if (buffer != nullptr) {
        auto *output = static_cast<short *>(buffer);
        for (DWORD index = 0; index < output_samples; ++index) {
            const double phase =
                kTau * stream->frequency *
                static_cast<double>(stream->sample_position + index) /
                kSampleRate;
            output[index] =
                static_cast<short>(std::sin(phase) * 12000.0);
        }
    }

    stream->sample_position += output_samples;
    DWORD output_bytes = output_samples * sizeof(short);
    if (stream->sample_position == stream->sample_count) {
        output_bytes |= BASS_STREAMPROC_END;
    }
    return output_bytes;
}

const ADDON_FUNCTIONS kAddonFunctions = {
    0,
    Free,
    GetLength,
    nullptr,
    nullptr,
    GetInfo,
    CanSetPosition,
    SetPosition,
    nullptr,
    nullptr,
    nullptr,
    nullptr,
    nullptr,
    nullptr,
    nullptr,
};

HSTREAM WINAPI CreateStream(BASSFILE file, DWORD flags) {
    char description[64] = {};
    const DWORD bytes_read =
        bassfunc->file.Read(file, description, sizeof(description) - 1);
    description[bytes_read] = '\0';

    unsigned int frequency = 0;
    unsigned int duration_ms = 0;
    if (std::sscanf(
            description,
            "BASSTONE\n%u\n%u",
            &frequency,
            &duration_ms
        ) != 2 ||
        frequency < 20 || frequency > 20000 || duration_ms == 0 ||
        duration_ms > 60000) {
        error(BASS_ERROR_FILEFORM);
    }

    auto *stream =
        static_cast<ToneStream *>(std::calloc(1, sizeof(ToneStream)));
    if (stream == nullptr) {
        error(BASS_ERROR_MEM);
    }
    stream->frequency = frequency;
    stream->sample_count =
        static_cast<QWORD>(kSampleRate) * duration_ms / 1000;

    flags &= BASS_SAMPLE_SOFTWARE | BASS_SAMPLE_LOOP | BASS_SAMPLE_3D |
             BASS_SAMPLE_FX | BASS_STREAM_DECODE | BASS_STREAM_AUTOFREE |
             0x3f000000;
    const HSTREAM handle = bassfunc->CreateStream(
        kSampleRate,
        1,
        flags,
        StreamProc,
        stream,
        &kAddonFunctions
    );
    if (handle == 0) {
        Free(stream);
        return 0;
    }

    bassfunc->file.SetStream(file, handle);
    noerrorn(handle);
}

}  // namespace

extern "C" __declspec(dllexport) const void *WINAPI
BASSplugin(DWORD face) {
    static const BASS_PLUGINFORM formats[] = {
        {kChannelType, "Example tone", "*.tone"},
    };
    static const BASS_PLUGININFO info = {
        kPluginVersion,
        1,
        formats,
    };

    switch (face) {
        case BASSPLUGIN_INFO:
            return &info;
        case BASSPLUGIN_CREATE:
            return reinterpret_cast<const void *>(CreateStream);
        default:
            return nullptr;
    }
}

BOOL WINAPI DllMain(HANDLE module, DWORD reason, LPVOID) {
    if (reason == DLL_PROCESS_ATTACH) {
        DisableThreadLibraryCalls(static_cast<HMODULE>(module));
        if (HIWORD(BASS_GetVersion()) != BASSVERSION || !GetBassFunc()) {
            return FALSE;
        }
    }
    return TRUE;
}
