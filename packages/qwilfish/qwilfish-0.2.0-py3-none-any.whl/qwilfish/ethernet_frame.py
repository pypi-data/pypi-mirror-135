# Local imports
from qwilfish.constants import DEFAULT_START_SYMBOL
from qwilfish.grammar import opts
from qwilfish.grammar_utils import srange
from qwilfish.grammar_utils import to_binstr
from qwilfish.grammar_utils import fix_tlv_length
from qwilfish.grammar_utils import gen_random_data

# TODO fuzz by changing endianness of fields and/or bytes
# TODO fuzz by inserting wrong TLVs

TL_BITLEN = 16 # number of bits for Type+Length fields

ETHERNET_FRAME_GRAMMAR = {
    DEFAULT_START_SYMBOL:
        [("<ethernet-frame>", opts(post=to_binstr))],
    "<ethernet-frame>":
        ["<addr><vlan-tags><type-payload>"],
    "<addr>":
        ["<dst><src>"],
    "<dst>":
        [("<byte><byte><byte><byte><byte><byte>", opts(prob=0.1)),
          "<mef-multicast>"
        ],
    "<mef-multicast>":
        ["x01x80xC2x00x00x00", "x01x80xC2x00x00x03", "x01x80xC2x00x00x0E"],
    "<src>":
        ["<byte><byte><byte><byte><byte><byte>"],
    "<vlan-tags>":
        ["", "<q-tag><vlan-tags>", "<q-tag>"],
    "<q-tag>":
        ["<tpid><pcp><dei><vlan>"],
    "<tpid>":
        ["x81x00", "x88xA8"],
    "<pcp>":
        ["<bit><bit><bit>"],
    "<dei>":
        ["<bit>"],
    "<vlan>":
        ["<byte><bit><bit><bit><bit>"],
    "<type-payload>":
        ["<lldp-ethertype><lldp-payload>"],
    "<byte>":
        ["x<hex><hex>"],
    "<hex>":
        srange("0123456789ABCDEF"),
    "<bit>":
        ["0", "1"],
    "<lldp-ethertype>":
        ["x88xCC"],
    "<lldp-payload>":
        ["<lldp-tlv-chassiid><lldp-tlv-portid><lldp-tlv-ttl><lldp-opt-tlvs>" \
         "<lldp-tlv-end>"
        ],
    "<lldp-opt-tlvs>":
        ["", "<lldp-opt-tlv>", "<lldp-opt-tlv><lldp-opt-tlvs>"],
    "<lldp-opt-tlv>"      :
        ["<lldp-tlv-portdesc>", "<lldp-tlv-sysname>", "<lldp-tlv-sysdesc>",
         "<lldp-tlv-syscap>", "<lldp-tlv-mgmtaddr>", "<lldp-tlv-custom>"
        ],
    "<tlv-len>":
        ["<bit><byte>"],
    "<lldp-tlv-end>":
        ["x00x00"],
    "<lldp-tlv-chassiid>":
        [("0000001<tlv-len><chassiid-subtype><chassiid-data>",
         opts(post=fix_tlv_length(TL_BITLEN)))
        ],
    "<chassiid-subtype>":
        ["00000001", "00000010", "00000011", "00000100", "00000101",
         "00000110", "00000111"
        ],
    "<chassiid-data>":
        [("", opts(pre=gen_random_data(0, 255)))],
    "<lldp-tlv-portid>":
        [("0000010<tlv-len><portid-subtype><portid-data>",
          opts(post=fix_tlv_length(TL_BITLEN)))
        ],
    "<portid-subtype>":
        ["00000001", "00000010", "00000011", "00000100", "00000101",
         "00000110", "00000111"
        ],
    "<portid-data>":
        [("", opts(pre=gen_random_data(0, 255)))],
    "<lldp-tlv-ttl>":
        [("0000011<tlv-len><byte><byte>",
          opts(post=fix_tlv_length(TL_BITLEN)))
        ],
    "<lldp-tlv-portdesc>":
        [""],
    "<lldp-tlv-sysname>" :
        [""],
    "<lldp-tlv-sysdesc>":
        [""],
    "<lldp-tlv-syscap>":
        [""],
    "<lldp-tlv-mgmtaddr>":
        [""],
    "<lldp-tlv-custom>":
        [""]
}
