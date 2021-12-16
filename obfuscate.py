"""

"""

import os.path as osp, os
import subprocess as sp
import base64
import zlib
from shutil import copyfile
try:
    from icecream import ic
    ic_err = False
except ImportError:
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)
    ic_err = True


DEBUG = False

if not DEBUG and not ic_err: ic.disable()
ROOT_PATH = osp.dirname(osp.realpath(__file__))
GEN_PATH = osp.join(ROOT_PATH, 'gen')

cpp_template = '''\
#include <string>
#include \"../include/obfuscate.h\"


int main(int argc, char* argv[]) {{
    std::string args;
    for (int i = 1; i < argc; i++) {{ args += std::string(" ") + argv[i]; }}
    std::string src = (std::string)AY_OBFUSCATE(R"({src})");
    std::string prefix = (std::string)AY_OBFUSCATE("echo \\"");
    std::string suffix = (std::string)AY_OBFUSCATE("\\" | python -B -c \\"exec(input())\\"");
    std::string cmd = prefix + src + suffix + args;
    int udRetCode = std::system(cmd.c_str());
    return WEXITSTATUS(udRetCode);
}}'''

def stickify(file_in_path):
    cmd = f'stickytape {file_in_path} --add-python-path {osp.dirname(file_in_path)}'
    return sp.run(cmd, shell = True, stdout = sp.PIPE, stderr = sp.STDOUT).stdout.decode(encoding='utf-8')

# def dumbify(file_in_path):
#     cmd = f'pyminifier --obfuscate {file_in_path}'
#     res = sp.run(cmd, shell = True, stdout = sp.PIPE, stderr = sp.STDOUT).stdout.decode(encoding='utf-8')
#     if '# Created by pyminifier (https://github.com/liftoff/pyminifier)' in res:
#         res = res.replace('# Created by pyminifier (https://github.com/liftoff/pyminifier)', '')

#     return res

def zipify(file_in_path):
    with open(file_in_path, 'r') as f:
        data = f.read()
        packed = base64.b64encode(zlib.compress(data.encode('utf-8'), 9)).decode('utf-8')
    return f'import zlib, base64; exec(zlib.decompress(base64.b64decode(\'{packed}\')))'


def obfuscate_file(file_path, output_name):
    copyfile(file_path, osp.join(GEN_PATH, 'source.py'))
    packaged_out_path = osp.join(GEN_PATH, '_packaged.py')
    #obfuscated_out_path = osp.join(GEN_PATH, '_obfuscated.py')
    zipped_out_path = osp.join(GEN_PATH, '_zipped.py')
    cpp_src_out_path = osp.join(GEN_PATH, 'main.cpp')
    executable_out_path = osp.join(GEN_PATH, output_name)
    hexdump_out_path = osp.join(GEN_PATH, '_hexdump.txt')
    bindump_out_path = osp.join(GEN_PATH, '_bindump.txt')
    
    with open(packaged_out_path, 'w') as f:
        sticky = stickify(file_path)
        sticky = '\n'.join(sticky.split('\n')[1:])
        f.write(sticky)

    # with open(obfuscated_out_path, 'w') as f:
    #     dumbed = dumbify(packaged_out_path)                
    #     f.write(dumbed)

    with open(zipped_out_path, 'w') as f:
        zipped = zipify(packaged_out_path)
        zipped = '; '.join(zipped.split('\n'))
        f.write(zipped)

    with open(cpp_src_out_path, 'w') as f:
        f.write(cpp_template.format(src = zipped))

    sp.run(f'g++ -std=c++14 {osp.basename(cpp_src_out_path)} -o {executable_out_path}', shell = True, cwd = GEN_PATH)
    sp.run(f'xxd {executable_out_path} > {hexdump_out_path}', shell = True)
    sp.run(f'xxd -b {executable_out_path} > {bindump_out_path}', shell = True)

def run(args):
    assert args.func == run
    input_path = args.input_path
    output_name = args.output_name
    assert osp.exists(input_path)
    assert input_path[-3:] == '.py'

    if not osp.exists(GEN_PATH):
        os.mkdir(GEN_PATH)

    obfuscate_file(osp.abspath(input_path), output_name)