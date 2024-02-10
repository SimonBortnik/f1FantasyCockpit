import { Chip } from "@mui/material";
import { nameDirectory } from "../services/idNameService";

export default function AvatarChip({id}) {
    return <Chip label={nameDirectory.get(id) ?? id}/>
}