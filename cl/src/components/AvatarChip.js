import { Avatar, Chip } from "@mui/material";
import { nameDirectory } from "../services/idNameService";
import { imageDirectory } from "../services/imageService";

export default function AvatarChip({id, onDelete}) {
    return <Chip size="medium" label={nameDirectory.get(id) ?? id} onDelete={onDelete} avatar={<Avatar sx={{ width: 32, height: 32 }} src={imageDirectory.get(id)}/>}/>
}